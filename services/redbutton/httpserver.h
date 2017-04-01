#pragma once

#include <microhttpd.h>


#define THREADPOOL_SIZE 4

class HttpRequestState;
class HttpRequestHandler;

struct HttpRequest
{
	HttpRequest();
	HttpRequest(const char *url, const char *method, MHD_Connection *connection);

	const char *url;
	const char *method;

	MHD_Connection *connection;
};

struct HttpResponse
{
	HttpResponse();
	HttpResponse(uint32_t code);
	HttpResponse(uint32_t code, char *content, size_t contentLength);

	uint32_t code;

	char *content;
	size_t contentLength;
};

class HttpServer
{
public:
	HttpServer(HttpRequestHandler *requestHandler);
	virtual ~HttpServer();

	void Start(uint32_t port);
	void Stop();

private:
	static int HandleRequest(void *param, MHD_Connection *connection, const char *url, const char *method, const char *version, const char *uploadData, size_t *uploadDataSize, void **context);
	static void PostProcessRequest(void *param, MHD_Connection *connection, void **context, MHD_RequestTerminationCode toe);
	static int SendResponse(MHD_Connection *connection, HttpResponse response);
	static void OnFatalError(void *param, const char *file, uint32_t line, const char *reason);

	bool isRunning;
	MHD_Daemon *daemon;
	HttpRequestHandler *requestHandler;
};

class HttpPostProcessor
{
public:
	virtual ~HttpPostProcessor();

	void CreateMhdProcessor();
	bool TryGetResponse(HttpResponse *response);

	virtual int IteratePostData(MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size) = 0;

	MHD_PostProcessor *mhdProcessor;

protected:
	HttpPostProcessor(HttpRequest request);

	void Complete(HttpResponse response);
	virtual void FinalizeRequest() = 0;

private:
	bool isCompleted;
	HttpRequest request;
	HttpResponse response;

	static int IteratePostDataBase(void *context, MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size);
};

#define OUT(x) NULL, sizeof(x), x

class HttpRequestHandler
{
public:
	virtual HttpResponse HandleGet(HttpRequest request) = 0;
	virtual HttpResponse HandlePost(HttpRequest request, HttpPostProcessor **postProcessor) = 0;

	static bool ParseUrl(const char *url, int parts, ...);
};