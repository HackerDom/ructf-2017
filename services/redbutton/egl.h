#pragma once
#include <EGL/egl.h>

//
struct Context
{
    EGLDisplay display = EGL_NO_DISPLAY;
    EGLSurface surface = EGL_NO_SURFACE;
    EGLContext context = EGL_NO_CONTEXT;
};


//
bool InitEGL();
void ShutdownEGL();
Context CreateLocalContext();
void MakeCurrentGlobalCtx();
void MakeCurrentLocalCtx( Context localCtx );
void MakeCurrentNullCtx();

//
bool CheckError( const char* errorMsgPrefix );