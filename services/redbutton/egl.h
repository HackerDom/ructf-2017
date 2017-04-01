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
EGLContext CreateLocalContext();

//
bool CheckError( const char* errorMsgPrefix );