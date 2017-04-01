#pragma once

#include "httpserver.h"
#include "detector.h"
#include "template.h"

class RequestHandler : public HttpRequestHandler
{
public:
	RequestHandler(DetectorStorage *detectors, TemplateStorage *templates);

	virtual HttpResponse HandleGet(HttpRequest request);
	virtual HttpResponse HandlePost(HttpRequest request, HttpPostProcessor **postProcessor);

private:
	DetectorStorage *detectors;
	TemplateStorage *templates;
};


class AddDetectorProcessor : public HttpPostProcessor
{
public:
	AddDetectorProcessor(HttpRequest request, DetectorStorage *detectors);
	virtual ~AddDetectorProcessor();

	virtual int IteratePostData(MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size);

	size_t dataSize;
	char *data;

private:
	DetectorStorage *detectors;	

	void FinalizeRequest();
};


class CheckDetectorProcessor : public HttpPostProcessor
{
public:
	CheckDetectorProcessor(HttpRequest request, Detector *detector);
	virtual ~CheckDetectorProcessor();

	virtual int IteratePostData(MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size);

	size_t dataSize;
	char *data;
	Detector *detector;
	uint32_t width;
	uint32_t height;

private:
	void FinalizeRequest();
};