#include "requesthandler.h"

#include <string.h>

RequestHandler::RequestHandler(DetectorStorage *detectors, TemplateStorage *templates)
{
	this->detectors = detectors;
	this->templates = templates;
}

HttpResponse RequestHandler::HandleGet(HttpRequest request)
{
	if (ParseUrl(request.url, 1, "detectors"))
	{
		int count;
		uuid *ids = detectors->ListDetectors(&count);

		int bufferSize = count * 64;
		char *buffer = new char[bufferSize];
		memset(buffer, 0, bufferSize);

		char idBuffer[64];
		char *bufferEnd = buffer;
		for (int i = 0; i < count; i++)
		{
			uuid_unparse(ids[i].bytes, idBuffer);
			strcat(idBuffer, "\n");

			strcpy(bufferEnd, idBuffer);
			bufferEnd += strlen(idBuffer);
		}

		return HttpResponse(MHD_HTTP_OK, buffer, strlen(buffer));
	}

	return HttpResponse(MHD_HTTP_NOT_FOUND);
}

HttpResponse RequestHandler::HandlePost(HttpRequest request, HttpPostProcessor **postProcessor)
{
	*postProcessor = NULL;

	if (ParseUrl(request.url, 2, "detectors", "add"))
	{
		printf(":: setting up AddDetectorProcessor\n");

		*postProcessor = new AddDetectorProcessor(request, detectors);

		return HttpResponse();
	}

	char id[64];
	if (ParseUrl(request.url, 3, "detectors", OUT(id), "check"))
	{
		return HttpResponse(MHD_HTTP_OK);
	}

	return HttpResponse(MHD_HTTP_NOT_FOUND);
}

AddDetectorProcessor::AddDetectorProcessor(HttpRequest request, DetectorStorage *detectors) : HttpPostProcessor(request)
{
	this->detectors = detectors;
}

AddDetectorProcessor::~AddDetectorProcessor()
{
	if (data)
	{
		delete[] data;
		data = NULL;
	}
}

int AddDetectorProcessor::IteratePostData(MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size)
{
	printf(":: iterating post fields, current = %s\n", key);

	if (!strcmp(key, "detector") && size > 0)
	{
		printf(":: found detector data, length = %ld\n", size);

		this->data = new char[size];

		memcpy(this->data, data + offset, size);

		dataSize = size;

		FinalizeRequest();
	}

	return MHD_YES;
}

void AddDetectorProcessor::FinalizeRequest()
{
	printf(":: finalizing request\n");

	if (!data)
	{
		Complete(HttpResponse(MHD_HTTP_BAD_REQUEST));
		return;
	}

	uuid id;
	uuid_generate(id.bytes);

	printf(":: adding detector: %ld, %.*s\n", dataSize, (int)dataSize, data);

	detectors->AddDetector(id, data, dataSize);

	char *responseData = new char[64];
	uuid_unparse(id.bytes, responseData);
	strcat(responseData, "\n");

	printf(":: added detector: %s", responseData);

	Complete(HttpResponse(MHD_HTTP_OK, responseData, strlen(responseData)));
}