#include <GLES2/gl2.h>
#include "egl.h"
#include <stdio.h>


#define ENABLE_RUNTIME_DEBUG 0


//
static const EGLint configAttribs[] = {
    EGL_SURFACE_TYPE, EGL_PBUFFER_BIT,
    EGL_BLUE_SIZE, 8,
    EGL_GREEN_SIZE, 8,
    EGL_RED_SIZE, 8,
    EGL_DEPTH_SIZE, 8,
    EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
    EGL_NONE
};


//
static const EGLint pbufferAttribs[] = {
    EGL_WIDTH, 8,
    EGL_HEIGHT, 8,
    EGL_NONE,
};


//
static const EGLint context_attribute_list[] = {
	EGL_CONTEXT_CLIENT_VERSION, 2,
#if ENABLE_RUNTIME_DEBUG
		EGL_CONTEXT_FLAGS_KHR, EGL_CONTEXT_OPENGL_DEBUG_BIT_KHR,
#endif
	EGL_NONE
};


//
void EGLAPIENTRY DebugOutput( GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar *message, const GLvoid *userParam )
{
	// const char* debSource = "";
	// const char* debType = "";
	// const char* debSev = "";

	// if( source == GL_DEBUG_SOURCE_API )
	// 	debSource = "OpenGL";
	// else if( source == GL_DEBUG_SOURCE_WINDOW_SYSTEM )
	// 	debSource = "Windows";
	// else if( source == GL_DEBUG_SOURCE_SHADER_COMPILER )
	// 	debSource = "Shader Compiler";
	// else if( source == GL_DEBUG_SOURCE_THIRD_PARTY )
	// 	debSource = "Third Party";
	// else if( source == GL_DEBUG_SOURCE_APPLICATION )
	// 	debSource = "Application";
	// else if( source == GL_DEBUG_SOURCE_OTHER )
	// 	debSource = "Other";

	// if( type == GL_DEBUG_TYPE_ERROR )
	// 	debType = "Error";
	// else if( type == GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR )
	// 	debType = "Deprecated behavior";
	// else if( type == GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR )
	// 	debType = "Undefined behavior";
	// else if( type == GL_DEBUG_TYPE_PORTABILITY )
	// 	debType = "Portability";
	// else if( type == GL_DEBUG_TYPE_PERFORMANCE )
	// 	debType = "Performance";
	// else if( type == GL_DEBUG_TYPE_OTHER )
	// 	debType = "Other";

	// bool showMes = true;
	// if( severity == GL_DEBUG_SEVERITY_HIGH )
	// 	debSev = "High";
	// else if( severity == GL_DEBUG_SEVERITY_MEDIUM )
	// 	debSev = "Medium";
	// else if( severity == GL_DEBUG_SEVERITY_LOW )
	// 	debSev = "Low";
	// else
	// 	showMes = false;

	// if( id == 131185 )
	// 	return;

	//printf( "OGLES debug:\n\tSource:%s\n\tType:%s\n\tID:%u\n\tSeverity:%s\n\tMessage:%s\n", debSource, debType, id, debSev, message );
	printf( "%s", message );
}


//
bool InitEGL( Context& ctx )
{
    ctx.display = eglGetDisplay( EGL_DEFAULT_DISPLAY );
    if( ctx.display == EGL_NO_DISPLAY ) {
        printf( "Error: No display found! 0x%X\n", eglGetError() );
        return false;
    }

    EGLint major, minor;
    if( !eglInitialize( ctx.display, &major, &minor ) ) {
        printf( "eglInitialize failed 0x%X\n", eglGetError() );
        return false;
    }

    printf( "EGL Version: \"%s\"\n", eglQueryString( ctx.display, EGL_VERSION ));
    printf( "EGL Vendor: \"%s\"\n", eglQueryString( ctx.display, EGL_VENDOR ));
    printf( "EGL Extensions: \"%s\"\n", eglQueryString( ctx.display, EGL_EXTENSIONS ));

    //
    EGLint numConfigs;
    EGLConfig eglCfg;
    eglChooseConfig( ctx.display, configAttribs, &eglCfg, 1, &numConfigs );

    //
    ctx.surface = eglCreatePbufferSurface( ctx.display, eglCfg, pbufferAttribs );
    if( ctx.surface == EGL_NO_SURFACE ){
        printf( "eglCreatePbufferSurface failed 0x%X\n", eglGetError() );
        return false;
    }

    //
    //eglBindAPI(EGL_OPENGL_API);

    //
    ctx.context = eglCreateContext( ctx.display, eglCfg, EGL_NO_CONTEXT, context_attribute_list );
    if( ctx.context == EGL_NO_CONTEXT ){
        printf( "eglCreateContext failed 0x%X\n", eglGetError() );
        return false;
    }

    eglMakeCurrent( ctx.display, ctx.surface, ctx.surface, ctx.context );

    printf("GL Vendor: \"%s\"\n", glGetString(GL_VENDOR));
	printf("GL Renderer: \"%s\"\n", glGetString(GL_RENDERER));
	printf("GL Version: \"%s\"\n", glGetString(GL_VERSION));
	printf("GL Extensions: \"%s\"\n", glGetString(GL_EXTENSIONS));


#if ENABLE_RUNTIME_DEBUG
	PFNDEBUG glDebugMessageCallback = ( PFNDEBUG )eglGetProcAddress( "glDebugMessageCallbackKHR" );
	glDebugMessageCallback( &DebugOutput, NULL );
	glEnable( GL_DEBUG_OUTPUT );
	glEnable( GL_DEBUG_OUTPUT_SYNCHRONOUS );
#endif

    return true;
}


//
void ShutdownEGL( const Context& ctx )
{
    eglTerminate( ctx.display );
}


//
bool CheckError( const char* errorMsgPrefix )
{
	GLenum err = glGetError();
	if( err != GL_NO_ERROR ) {
		fprintf( stderr, "%s: %x\n", errorMsgPrefix, err );
		return false;
	}

	return true;
}