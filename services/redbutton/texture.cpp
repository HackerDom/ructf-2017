#include <stdio.h>
#include "glwrap.h"


//
struct TextureFormat
{
	GLint internalFormat;
	GLint format;
	GLint type;
} g_mapFormatToTextureFormat[] = {
	{ GL_ALPHA, GL_ALPHA, GL_UNSIGNED_BYTE },
	{ GL_RGBA, GL_RGBA, GL_UNSIGNED_BYTE },
};


//
Texture2D::Texture2D( int width, int height, Format format, void* initData )
	: m_width( width ), m_height( height ), m_format( format )
{
	glGenTextures( 1, &m_texture );
	glBindTexture( GL_TEXTURE_2D, m_texture );

	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST );
 

	TextureFormat fmt = g_mapFormatToTextureFormat[ m_format ];

	glTexImage2D( GL_TEXTURE_2D, 0, fmt.internalFormat, m_width, m_height, 0, fmt.format, fmt.type, NULL );

	if( !CheckError( "Failed to create texture" ) ) {
		glDeleteTextures( 1, &m_texture );
		m_texture = 0;
	}

	glGenFramebuffers( 1, &m_framebuffer );
	glBindFramebuffer( GL_FRAMEBUFFER, m_framebuffer );
	glFramebufferTexture2D( GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, m_texture, 0 );
	glBindFramebuffer( GL_FRAMEBUFFER, 0 );

	if( !CheckError( "Failed to create framebuffer" ) ) {
		glDeleteTextures( 1, &m_texture );
		glDeleteFramebuffers( 1, &m_framebuffer );
		m_texture = 0;
		m_framebuffer = 0;
	}
}


//
Texture2D::Texture2D( const Image& image )
	: Texture2D( image.width, image.height, FORMAT_RGBA, ( void* )image.rgba )
{
	
}


//
Texture2D::~Texture2D()
{
	glDeleteTextures( 1, &m_texture );
	glDeleteFramebuffers( 1, &m_framebuffer );
	m_texture = 0;
	m_framebuffer = 0;
}


//
GLuint Texture2D::GetTexture() const
{
	return m_texture;
}


//
GLuint Texture2D::GetFramebuffer() const
{
	return m_framebuffer;
}


//
int Texture2D::GetWidth() const
{
	return m_width;
}


//
int Texture2D::GetHeight() const
{
	return m_height;
}
