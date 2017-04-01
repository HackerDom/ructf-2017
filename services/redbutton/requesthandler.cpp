#include "requesthandler.h"
#include "glwrap.h"

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

	char idBuffer[64];
	if (ParseUrl(request.url, 3, "detectors", OUT(idBuffer), "check"))
	{
		uuid id;
		uuid_parse(idBuffer, id.bytes);

		printf(":: searching for detector %s...\n", idBuffer);

		Detector *detector = detectors->GetDetector(id);

		if (!detector)
			return HttpResponse(MHD_HTTP_NOT_FOUND);

		printf(":: setting up CheckDetectorProcessor\n");

		*postProcessor = new CheckDetectorProcessor(request, detector);

		return HttpResponse();
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

CheckDetectorProcessor::CheckDetectorProcessor(HttpRequest request, Detector *detector) : HttpPostProcessor(request)
{
	this->detector = detector;
	this->data = NULL;

	width = 0;
	height = 0;
}

CheckDetectorProcessor::~CheckDetectorProcessor()
{
	if (data)
	{
		delete[] data;
		data = NULL;
	}
}

int CheckDetectorProcessor::IteratePostData(MHD_ValueKind kind, const char *key, const char *filename, const char *contentType, const char *transferEncoding, const char *data, uint64_t offset, size_t size)
{
	printf(":: iterating post fields, current = %s\n", key);

	if (!strcmp(key, "image") && size > 0)
	{
		printf(":: found image data, length = %ld\n", size);

		this->data = new char[size];

		memcpy(this->data, data + offset, size);

		dataSize = size;
	}

	if (!strcmp(key, "w") && size > 0)
	{
		printf(":: found out width, length = %ld\n", size);

		char buffer[16];

		if (size > sizeof(buffer))
			return MHD_NO;

		memset(buffer, 0, sizeof(buffer));
		memcpy(buffer, data + offset, size);

		width = atoi(buffer);
	}

	if (!strcmp(key, "h") && size > 0)
	{
		printf(":: found out height, length = %ld\n", size);

		char buffer[16];

		if (size > sizeof(buffer))
			return MHD_NO;

		memset(buffer, 0, sizeof(buffer));
		memcpy(buffer, data + offset, size);

		height = atoi(buffer);
	}

	if (data)
		FinalizeRequest();

	return MHD_YES;
}

void CheckDetectorProcessor::FinalizeRequest()
{
	printf(":: finalizing request\n");

	if (!data)
	{
		Complete(HttpResponse(MHD_HTTP_BAD_REQUEST));
		return;
	}

	static GLfloat vVertices[] = {  -1.0f,  1.0f, 0.0f,
                                 1.0f,  1.0f, 0.0f,
                                 1.0f, -1.0f, 0.0f,
                                -1.0f,  1.0f, 0.0f,
                                 1.0f, -1.0f, 0.0f,
                                -1.0f, -1.0f, 0.0f };

    Texture2D texture( data, dataSize );

    VertexShader vs( "shaders/simple.vert", false );
    //FragmentShader fs( detector->data, detector->length );
    FragmentShader fs( ( const char* )detector->data );
    Program pr( vs, fs );

    if( pr.GetProgram() == 0 ){
    	printf(":: invalid program\n" );
		Complete(HttpResponse(MHD_HTTP_BAD_REQUEST));
    	return;
    }

    pr.SetTexture( "tex", texture );
    pr.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );

   	int w = width > 0 ? width : 4;
    int h = height > 0 ? height : 1;
    Texture2D target( w, h, FORMAT_RGBA );

    BindFramebuffer( target );
    Clear( 0.0, 0.0, 0.0, 0.0 );

    SetProgram( pr ); 
    glDrawArrays( GL_TRIANGLES, 0, 6 );

    target.ReadBack();
    save_png( "output.png", target.GetRGBA(), target.GetWidth(), target.GetHeight() );

	Complete(HttpResponse(MHD_HTTP_OK));
}