#include "httpserver.h"

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <microhttpd.h>
#include <pthread.h>

#define POSTBUFFERSIZE  65536

HttpServer::HttpServer(HttpRequestHandler *requestHandler)
{
	this->requestHandler = requestHandler;
	isRunning = false;
}

HttpServer::~HttpServer()
{
	Stop();
}

void HttpServer::Start(uint32_t port)
{
	if (isRunning)
		return;

	MHD_set_panic_func(OnFatalError, NULL);

	daemon = MHD_start_daemon(
		MHD_USE_SELECT_INTERNALLY,
		port, NULL, NULL, HandleRequest, this, 
		MHD_OPTION_THREAD_POOL_SIZE, THREADPOOL_SIZE, 
	// TODO increase 
		MHD_OPTION_CONNECTION_TIMEOUT, 5u,
		MHD_OPTION_NOTIFY_COMPLETED, PostProcessRequest, NULL,
		MHD_OPTION_END);

	if (!daemon)
	{
		printf("Failed to start MHD_Daemon!\n");
		exit(1);
	}

	printf(":: current thread id = %ld\n", pthread_self());

	printf("Listening on port %d...\n", port);

	isRunning = true;
}

void HttpServer::Stop()
{
	if (!isRunning)
		return;

	MHD_stop_daemon(daemon);

	isRunning = false;
}

int HttpServer::HandleRequest(void *param, MHD_Connection *connection, const char *url, const char *method, const char *version, const char *uploadData, size_t *uploadDataSize, void **context)
{
	HttpServer *self = (HttpServer *)param;

	printf(":: current thread id = %ld\n", pthread_self());

	printf("Received request: %s %s\n", method, url);

	if (!*context)
	{
		if (!strcmp(method, "POST"))
		{
			HttpPostProcessor *postProcessor = NULL;

			HttpResponse response = self->requestHandler->HandlePost(HttpRequest(url, method, connection), &postProcessor);

			if (!postProcessor)
			{
				SendResponse(connection, response);
				return MHD_YES;
			}

			postProcessor->CreateMhdProcessor();

			*context = postProcessor;

			return MHD_YES;
		}
	}

	if (!strcmp (method, "GET"))
	{
		SendResponse(connection, self->requestHandler->HandleGet(HttpRequest(url, method, connection)));

		return MHD_YES;
	}

	if (!strcmp (method, "POST"))
	{
		HttpPostProcessor *postProcessor = (HttpPostProcessor *)*context;

		int result = MHD_YES;

		if (*uploadDataSize != 0)
		{
			result = MHD_post_process(postProcessor->mhdProcessor, uploadData, *uploadDataSize);

			*uploadDataSize = 0;
		}
		else
		{
			HttpResponse response;
			if (postProcessor->TryGetResponse(&response))
				SendResponse(connection, response);
		}


		return result;
	}

	SendResponse(connection, HttpResponse(MHD_HTTP_NOT_IMPLEMENTED));
}

void HttpServer::PostProcessRequest(void *param, MHD_Connection *connection, void **context, MHD_RequestTerminationCode toe)
{
	printf(":: post process request started\n");

	HttpPostProcessor *postProcessor = (HttpPostProcessor *)*context;

	if (!postProcessor)
		return;

	delete postProcessor;
	*context = NULL;
}

int HttpServer::SendResponse(MHD_Connection *connection, HttpResponse response)
{
	printf(":: send response: %.*s", (int)response.contentLength, response.content);

	MHD_Response *mhdResponse = MHD_create_response_from_buffer(response.contentLength, response.content, MHD_RESPMEM_MUST_COPY);

	if (!mhdResponse)
		return MHD_NO;

	int result = MHD_queue_response(connection, response.code, mhdResponse);

	MHD_destroy_response(mhdResponse);

	delete[] response.content;

	return result;
}

void HttpServer::OnFatalError(void *param, const char *file, uint32_t line, const char *reason)
{
	printf("Fatal: %s at %s, line %d\n", reason, file, line);
	exit(1);
}

HttpPostProcessor::HttpPostProcessor(HttpRequest request)
{
	this->request = request;
	isCompleted = false;
}

void HttpPostProcessor::CreateMhdProcessor()
{
	mhdProcessor = MHD_create_post_processor(request.connection, POSTBUFFERSIZE, IteratePostDataBase, (void *)this);
}

bool HttpPostProcessor::TryGetResponse(HttpResponse *response)
{
	if (!this->response.code)
		FinalizeRequest();

	if (!isCompleted)
		return false;

	*response = this->response;

	isCompleted = false;

	return true;
}

void HttpPostProcessor::Complete(HttpResponse response)
{
	if (isCompleted)
		return;

	this->response = response;

	isCompleted = true;
}

HttpPostProcessor::~HttpPostProcessor()
{
	if (mhdProcessor)
	{
		MHD_destroy_post_processor(mhdProcessor);
		mhdProcessor = NULL;
	}
}

int HttpPostProcessor::IteratePostDataBase(void *context, MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size)
{
	HttpPostProcessor *self = (HttpPostProcessor *)context;

	if (!self)
		return MHD_NO;

	return self->IteratePostData(kind, key, filename, contentType, transferEncoding, data, offset, size);
}

HttpRequest::HttpRequest()
{
	this->url = NULL;
	this->method = NULL;
	this->connection = NULL;
};

HttpRequest::HttpRequest(const char *url, const char *method, MHD_Connection *connection)
{
	this->url = url;
	this->method = method;
	this->connection = connection;
};

HttpResponse::HttpResponse() : HttpResponse(0, NULL, 0)
{
}

HttpResponse::HttpResponse(uint32_t code) : HttpResponse(code, NULL, 0)
{
}

HttpResponse::HttpResponse(uint32_t code, char *content, size_t contentLength)
{
	this->code = code;
	this->content = content;
	this->contentLength = contentLength;
}

bool HttpRequestHandler::ParseUrl(const char *url, int parts, ...)
{
	if (url[0] != '/')
		return false;

	va_list args;

	va_start(args, parts);

	bool result = true;

	const char *position = url + 1;
	for (int i = 0; i < parts; i++)
	{
		const char *nextSlash = strchr(position, '/');

		if (!nextSlash)
		{
			if (i != parts - 1)
			{
				result = false;
				break;
			}

			nextSlash = strchr(position, '\0');
		}

		int partLength = nextSlash - position;

		const char *part = va_arg(args, const char *);

		if (!part)
		{
			size_t size = va_arg(args, size_t);

			if (partLength >= size)
			{
				result = false;
				break;
			}

			strncpy(va_arg(args, char *), position, partLength);
		}
		else
		{
			if (strlen(part) != partLength)
			{
				result = false;
				break;
			}

			if (strncmp(part, position, partLength))
			{
				result = false;
				break;
			}
		}

		position = nextSlash + 1;
	}

	va_end(args);

	return result;
}