#include "requesthandler.h"
#include "glwrap.h"
#include "spin_lock.h"
#include "allocator.h"

#include <string.h>

//
struct ContextInfo
{
	Context context;
	pthread_t thread;
};
ContextInfo g_contexts[ THREADPOOL_SIZE ];
Lock 	g_contextLock;


//
Context GetContext()
{
	AutoLock autoLock( g_contextLock );

	Context ctx;
	pthread_t tid = pthread_self();

	bool found = false;

	for (int i = 0; i < THREADPOOL_SIZE; i++)
	{
		if (g_contexts[i].thread == tid)
		{
			ctx = g_contexts[i].context;
			printf( ":: old thread %lx ctx %d\n", tid, i );
			found = true;
			break;
		}
	}

	if (!found)
	{
		for (int i = 0; i < THREADPOOL_SIZE; i++)
		{
			if (g_contexts[i].thread == 0)
			{
				g_contexts[i].thread = tid;
				ctx = g_contexts[i].context;
				printf( ":: new thread %lx ctx %d\n", tid, i );
				found = true;
				break;
			}
		}
	}

	if (!found)
	{
		printf(":: NO AVAILABLE CONTEXT\n");
		exit(1);
	}

	return ctx;
}


//
RequestHandler::RequestHandler(DetectorStorage *detectors)
{
	this->detectors = detectors;

	for( int i = 0; i < THREADPOOL_SIZE; i++ )
	{
		g_contexts[ i ].context = CreateLocalContext();
		g_contexts[ i ].thread = 0;
	}
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
	memset(idBuffer, 0, sizeof(idBuffer));
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
		printf(":: found detector data, length = %d\n", size);

		this->data = new char[size];

		memcpy(this->data, data + offset, size);

		dataSize = size;
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

	printf(":: adding detector: %d\n", dataSize );

	detectors->AddDetector(id, data, dataSize);

	char *responseData = new char[64];
	uuid_unparse(id.bytes, responseData);
	strcat(responseData, "\n");

	printf(":: added detector: %s", responseData);

	Complete(HttpResponse(MHD_HTTP_OK, responseData, strlen(responseData)));
}

CheckDetectorProcessor::CheckDetectorProcessor(HttpRequest request, Detector *detector ) : HttpPostProcessor(request)
{
	this->detector = detector;
	this->data = NULL;
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
		printf(":: found image data, length = %d\n", size);
		printf(":: filename = %s\n", filename);

		this->data = new char[size];

		memcpy(this->data, data + offset, size);

		dataSize = size;
	}

	return MHD_YES;
}

void CheckDetectorProcessor::FinalizeRequest()
{
	printf(":: finalizing request, data = %p\n", data);

	if (!data)
	{
		Complete(HttpResponse(MHD_HTTP_BAD_REQUEST));
		return;
	}

	timespec tp;
	double startTime, endTime;
	clock_gettime( CLOCK_REALTIME, &tp );
	startTime = tp.tv_sec + tp.tv_nsec / 1000000000.0;

	
	Context ctx = GetContext();
	MakeCurrentLocalCtx( ctx );

	static GLfloat vVertices[] = {  -1.0f,  1.0f, 0.0f,
                                 1.0f,  1.0f, 0.0f,
                                 1.0f, -1.0f, 0.0f,
                                -1.0f,  1.0f, 0.0f,
                                 1.0f, -1.0f, 0.0f,
                                -1.0f, -1.0f, 0.0f };

    static GLfloat vUv[] = {   0.0f, 1.0f,
                    1.0f, 1.0f,
                    1.0f, 0.0f,
                    0.0f, 1.0f,
                    1.0f, 0.0f,
                    0.0f, 0.0f
					};


#if DEBUG
	PrintMap();
#endif

	{
		Texture2D texture( data, dataSize );
		if( texture.GetTexture() == 0 ){ 
			printf(":: failed to create texture\n" );
			Complete(HttpResponse(MHD_HTTP_BAD_REQUEST));
	    	return;
		}

		
	#if DEBUG
		save_png( "input.png", texture.GetRGBA(), texture.GetWidth(), texture.GetHeight() );
		{
			FILE* f = fopen( "flag.bin", "w" );
			fwrite( (const void *)detector->shader, (uint32_t)detector->shaderSize, 1, f );
			fclose( f );
		}
	#endif

	    VertexShader vs( "shaders/simple.vert", false );
	    FragmentShader fs( (const void *)detector->shader, (uint32_t)detector->shaderSize );
	    Program pr( vs, fs );

	    if( pr.GetProgram() == 0 ){
	    	printf(":: invalid program\n" );
			Complete(HttpResponse(MHD_HTTP_BAD_REQUEST));
	    	return;
	    }

	    pr.SetTexture( "tex", texture );
	    pr.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );
	    pr.SetAttribute( "v_uv", 2, GL_FLOAT, GL_FALSE, 0, vUv, 6 * 2 * sizeof( GLfloat ) );

	    const int w = detector->targetWidth;
	    const int h = detector->targetHeight;
	    const int targetSize = w * h * sizeof( RGBA );
	    Texture2D target( w, h, FORMAT_RGBA );
	    if( target.GetTexture() == 0 ){
			printf(":: failed to create target texture\n" );
			Complete(HttpResponse(MHD_HTTP_BAD_REQUEST));
	    	return;
		}

	    BindFramebuffer( target );
	    Clear( 0.0, 0.0, 0.0, 0.0 );

	    SetProgram( pr ); 
	    glDrawArrays( GL_TRIANGLES, 0, 6 );

	    target.ReadBack();

	    clock_gettime( CLOCK_REALTIME, &tp );
		endTime = tp.tv_sec + tp.tv_nsec / 1000000000.0;
		printf( ":: Time: %f\n", endTime - startTime );

	    char *responseData = (char *)target.GetRGBA();
	    char *dataCopy = new char[ targetSize ];
	    memcpy(dataCopy, responseData, targetSize );

	    printf(":: returning response %d\n", targetSize );
		Complete(HttpResponse(MHD_HTTP_OK, dataCopy, targetSize ));
	}

	MakeCurrentNullCtx();
}
