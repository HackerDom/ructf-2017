#include "httpserver.h"

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <microhttpd.h>

#define POSTBUFFERSIZE  65536

HttpServer::HttpServer(HttpRequestHandler *requestHandler)
{
	this->requestHandler = requestHandler;
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

	daemon = MHD_start_daemon(MHD_USE_THREAD_PER_CONNECTION, port, NULL, NULL, HandleRequest, this, 
		MHD_OPTION_CONNECTION_TIMEOUT, 1u,
		MHD_OPTION_NOTIFY_COMPLETED, PostProcessRequest, NULL,
		MHD_OPTION_END);

	if (!daemon)
	{
		printf("Failed to start MHD_Daemon!\n");
		exit(1);
	}

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

	printf("Received request: %s %s\n", method, url);

	if (!*context)
	{
		if (!strcmp(method, "POST"))
		{
			HttpStateData *userData = NULL;
			PostIterator postIterator = NULL;
			PostFinalizer postFinalizer = NULL;

			HttpResponse response = self->requestHandler->HandlePost(HttpRequest(url, method, connection), &userData, &postIterator, &postFinalizer);

			if (!postFinalizer)
			{
				SendResponse(connection, response);
				return MHD_YES;
			}

			HttpRequestState *state = new HttpRequestState(HttpRequest(url, method, connection), self->requestHandler, postIterator, postFinalizer, userData);

			*context = state;

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
		HttpRequestState *state = (HttpRequestState *)*context;

		if (*uploadDataSize != 0)
		{
			MHD_post_process(state->postProcessor, uploadData, *uploadDataSize);

			*uploadDataSize = 0;
		}

		return MHD_YES;
	}

	SendResponse(connection, HttpResponse(MHD_HTTP_NOT_IMPLEMENTED));
}

void HttpServer::PostProcessRequest(void *param, MHD_Connection *connection, void **context, MHD_RequestTerminationCode toe)
{
	HttpRequestState *state = (HttpRequestState *)*context;

	if (!state)
		return;

	HttpResponse response = (state->requestHandler->*state->postFinalizer)(state);

	SendResponse(connection, response);

	delete state;
	*context = NULL;
}

int HttpServer::SendResponse(MHD_Connection *connection, HttpResponse response)
{
	MHD_Response *mhdResponse = MHD_create_response_from_buffer(response.contentLength, response.content, MHD_RESPMEM_PERSISTENT);

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

HttpRequestState::HttpRequestState(HttpRequest request, HttpRequestHandler *requestHandler, PostIterator postIterator, PostFinalizer postFinalizer, HttpStateData *userData)
{
	this->request = request;
	this->requestHandler = requestHandler;
	this->postIterator = postIterator;
	this->postFinalizer = postFinalizer;
	this->userData = userData;

	postProcessor = MHD_create_post_processor(request.connection, POSTBUFFERSIZE, IteratePostData, (void *)this);
}

HttpRequestState::~HttpRequestState()
{
	if (postProcessor)
	{
		MHD_destroy_post_processor(postProcessor);
		postProcessor = NULL;
	}

	if (userData)
	{
		delete userData;
		userData = NULL;
	}
}

int HttpRequestState::IteratePostData(void *context, MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size)
{
	HttpRequestState *state = (HttpRequestState *)context;

	if (!state)
		return MHD_NO;

	return (state->requestHandler->*state->postIterator)(state, kind, key, filename, contentType, transferEncoding, data, offset, size);
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

HttpResponse::HttpResponse(uint32_t code)
{
	this->code = code;
	this->content = NULL;
	this-> contentLength = 0;
}

HttpResponse::HttpResponse(uint32_t code, char *content, size_t contentLength)
{
	this->code = code;
	this->content = content;
	this->contentLength = contentLength;
}