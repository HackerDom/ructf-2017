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
bool InitEGL( Context& ctx );
void ShutdownEGL( const Context& ctx );

//
bool CheckError( const char* errorMsgPrefix );