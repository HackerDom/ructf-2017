#pragma once
#include <EGL/egl.h>

//
struct Context
{
    EGLDisplay display = EGL_NO_DISPLAY;
    EGLSurface surface = EGL_NO_SURFACE;
    EGLContext context = EGL_NO_CONTEXT;
    EGLConfig eglCfg;
};


//
bool InitEGL();
void ShutdownEGL();
EGLContext CreateLocalContext();
void MakeCurrentGlobalCtx();
void MakeCurrentLocalCtx( EGLContext localCtx );
void MakeCurrentNullCtx();

//
bool CheckError( const char* errorMsgPrefix );