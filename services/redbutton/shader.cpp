#include <GLES2/gl2.h>
#include <stdio.h>
#include <string.h>
#include "shader.h"
#include "egl.h"


//
Shader::Shader( GLuint type, const char* fileName )
{
	printf( "Create shader %s\n", fileName );
	FILE* f = fopen( fileName, "r" );
	if( !f )
		return;

	fseek( f, 0, SEEK_END );
	size_t fileSize = ftell( f );
	fseek( f, 0, SEEK_SET );
	char* shaderSource = new char[ fileSize + 1 ];
	memset( shaderSource, 0, fileSize + 1 );
	fread( shaderSource, 1, fileSize, f );
	fclose( f );

	m_shader = glCreateShader( type );
	if( !m_shader ) {
		fprintf( stderr, "Error: glCreateShader failed: 0x%08X\n", glGetError());
		return;
	}

	glShaderSource( m_shader, 1, &shaderSource, NULL );
	glCompileShader( m_shader );

	GLint ret;
	glGetShaderiv( m_shader, GL_COMPILE_STATUS, &ret );
	if( !ret ) {
		char *log;

		fprintf( stderr, "Error: %s shader compilation failed!\n", fileName );
		glGetShaderiv( m_shader, GL_INFO_LOG_LENGTH, &ret );

		if( ret > 1 ) {
			log = new char[ ret ];
			glGetShaderInfoLog( m_shader, ret, NULL, log );
			fprintf( stderr, "%s\n", log );
			delete[] log;
		}

		glDeleteShader( m_shader );
		m_shader = 0;
	}
}


//
Shader::~Shader()
{
	glDeleteShader( m_shader );
}


//
GLuint Shader::GetShader() const
{
	return m_shader;
}


//
bool Shader::IsValid() const
{
	return m_shader != 0;
}


//
VertexShader::VertexShader( const char* fileName )
	: Shader( GL_VERTEX_SHADER, fileName )
{

}


//
FragmentShader::FragmentShader( const char* fileName )
	: Shader( GL_FRAGMENT_SHADER, fileName )
{

}


//
Program::Program( const VertexShader& vs, const FragmentShader& fs, const char** attributeList, int attributesNum )
	: m_vs( vs )
	, m_fs( fs )
{
	m_program = glCreateProgram();
	if( !m_program ) {
		fprintf( stderr, "Error: failed to create m_program!\n" );
		return;
	}

	glAttachShader( m_program, vs.GetShader() );
	glAttachShader( m_program, fs.GetShader() );

	for( int i = 0; i < attributesNum; i++ ) 
		glBindAttribLocation( m_program, i, attributeList[ i ] );
	
	glLinkProgram( m_program );

	GLint ret;
	glGetProgramiv( m_program, GL_LINK_STATUS, &ret );
	if( !ret ) {
		char *log;

		fprintf( stderr, "Error: m_program linking failed!\n" );
		glGetProgramiv( m_program, GL_INFO_LOG_LENGTH, &ret );

		if( ret > 1 ) {
			log = new char[ ret ];
			glGetProgramInfoLog( m_program, ret, NULL, log );
			fprintf( stderr, "%s", log );
			delete[] log;
		}
		return;
	}

	glUseProgram( 0 );
}


//
GLuint Program::GetProgram() const
{
	return m_program;
}