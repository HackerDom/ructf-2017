#include <GLES2/gl2.h>
#include <stdio.h>
#include "texture.h"
#include "egl.h"


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
Texture2D::Texture2D( int width, int height, Format format )
{
	glGenTextures( 1, &m_texture );
	glBindTexture( GL_TEXTURE_2D, m_texture );

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
 

	TextureFormat fmt = g_mapFormatToTextureFormat[ format ];

	glTexImage2D( GL_TEXTURE_2D, 0, fmt.internalFormat, width, height, 0, fmt.format, fmt.type, NULL );

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
