#include "glwrap.h"


//
const Texture2D* g_curFramebuffer = nullptr;


//
void SetProgram( const Program& p )
{
	glUseProgram( p.GetProgram() );
	p.BindUniforms();
}


//
void BindFramebuffer( const Texture2D& t )
{
	glBindFramebuffer( GL_FRAMEBUFFER, t.GetFramebuffer() );
    glViewport( 0, 0, t.GetWidth(), t.GetHeight() );

    g_curFramebuffer = &t;
}


//
void Clear( float r, float g, float b, float a )
{
	glClearColor( r, g, b, a );
	glClear( GL_COLOR_BUFFER_BIT );
}


//
void ReadPixels( Image& i )
{
	glPixelStorei( GL_PACK_ALIGNMENT, 1 );
    i.Reinit( g_curFramebuffer->GetWidth(), g_curFramebuffer->GetHeight() );
    glReadPixels( 0, 0, g_curFramebuffer->GetWidth(), g_curFramebuffer->GetHeight(), GL_RGBA, GL_UNSIGNED_BYTE, ( GLvoid* )i.rgba );
    CheckError( "glReadPixels failed" );
}