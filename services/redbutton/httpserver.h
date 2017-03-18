#pragma once

#include <microhttpd.h>


class HttpStateData;
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

typedef int (HttpRequestHandler:: *PostIterator)(HttpRequestState *state, MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size);
typedef HttpResponse (HttpRequestHandler:: *PostFinalizer)(HttpRequestState *state);

class HttpRequestHandler
{
public:
	virtual HttpResponse HandleGet(HttpRequest request) = 0;
	virtual HttpResponse HandlePost(HttpRequest request, HttpStateData **userData, PostIterator *postIterator, PostFinalizer *postFinalizer) = 0;
};

class HttpRequestState
{
public:
	HttpRequestState(HttpRequest request, HttpRequestHandler *requestHandler, PostIterator postIterator, PostFinalizer postFinalizer, HttpStateData *userData);
	virtual ~HttpRequestState();
	
	HttpRequest request;
	HttpStateData *userData;
	PostIterator postIterator;
	PostFinalizer postFinalizer;
	MHD_PostProcessor *postProcessor;
	HttpRequestHandler *requestHandler;

private:
	static int IteratePostData(void *context, MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size);
};

class HttpStateData
{
};