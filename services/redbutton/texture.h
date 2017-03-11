#pragma once


//
enum Format
{
	FORMAT_A8,
	FORMAT_RGBA,
	FORMAT_COUNT
};


//
class Texture2D
{
public:
	//
	Texture2D() = delete;
	Texture2D( int width, int height, Format format );
	~Texture2D();


	//
	GLuint GetTexture() const;
	GLuint GetFramebuffer() const;

private:
	//
	GLuint m_texture = 0;
	GLuint m_framebuffer = 0;
};