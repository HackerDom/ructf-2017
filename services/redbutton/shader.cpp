#include <stdio.h>
#include <string.h>
#include "glwrap.h"


//
Shader::Shader( GLuint type, const char* fileName, bool isBinary )
{
	printf( "Create shader %s\n", fileName );
	FILE* f = fopen( fileName, "r" );
	if( !f ){
		printf( "Shader file not found %s\n", fileName );
		return;
	}

	fseek( f, 0, SEEK_END );
	size_t fileSize = ftell( f );
	fseek( f, 0, SEEK_SET );
	char* fileData = new char[ fileSize + 1 ];
	memset( fileData, 0, fileSize + 1 );
	fread( fileData, 1, fileSize, f );
	fclose( f );

	m_shader = glCreateShader( type );
	if( !m_shader ) {
		fprintf( stderr, "Error: glCreateShader failed: 0x%08X\n", glGetError());
		return;
	}

	if( isBinary ){
		glShaderBinary( 1, &m_shader, GL_MALI_SHADER_BINARY_ARM, fileData, fileSize );
		if( !CheckError( "Failed to create shader from binary" ) ) {
			glDeleteShader( m_shader );
			m_shader = 0;
	}
	}
	else {
		glShaderSource( m_shader, 1, &fileData, NULL );
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
}


//
Shader::Shader( GLuint type, const char* shader )
{
	m_shader = glCreateShader( type );
	if( !m_shader ) {
		fprintf( stderr, "Error: glCreateShader failed: 0x%08X\n", glGetError());
		return;
	}

	glShaderSource( m_shader, 1, &shader, NULL );
	glCompileShader( m_shader );

	GLint ret;
	glGetShaderiv( m_shader, GL_COMPILE_STATUS, &ret );
	if( !ret ) {
		char *log;

		fprintf( stderr, "Error: shader compilation failed!\n" );
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
Shader::Shader( GLuint type, const void* binary, uint32_t binarySize )
{
	m_shader = glCreateShader( type );
	if( !m_shader ) {
		fprintf( stderr, "Error: glCreateShader failed: 0x%08X\n", glGetError());
		return;
	}

	glShaderBinary( 1, &m_shader, GL_MALI_SHADER_BINARY_ARM, binary, binarySize );
	if( !CheckError( "Failed to create shader from binary" ) ) {
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
VertexShader::VertexShader( const char* fileName, bool isBinary )
	: Shader( GL_VERTEX_SHADER, fileName, isBinary )
{

}


//
VertexShader::VertexShader( const void* binary, uint32_t binarySize )
	: Shader( GL_VERTEX_SHADER, binary, binarySize )
{

}


//
FragmentShader::FragmentShader( const char* fileName, bool isBinary )
	: Shader( GL_FRAGMENT_SHADER, fileName, isBinary )
{

}


//
FragmentShader::FragmentShader( const char* shader )
	: Shader( GL_FRAGMENT_SHADER, shader )
{

}


//
FragmentShader::FragmentShader( const void* binary, uint32_t binarySize )
	: Shader( GL_FRAGMENT_SHADER, binary, binarySize )
{

}


//
Program::Program( const VertexShader& vs, const FragmentShader& fs )
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

	GLint attrNum = 0;
	glGetProgramiv( m_program, GL_ACTIVE_ATTRIBUTES, &attrNum );
	for( GLint i = 0; i < attrNum; i++ )
	{
		const int attrNameSize = 256;
		char attrName[ attrNameSize ];
		memset( attrName, 0, attrNameSize );
		glGetActiveAttrib( m_program, i, attrNameSize, nullptr, nullptr, nullptr, attrName );
		GLint attrLocation = glGetAttribLocation( m_program, attrName );

		VertexAttribute attr;
		m_attributes[ attrLocation ] = attr;
	}

	glUseProgram( 0 );
}


//
Program::~Program()
{
	glDeleteProgram( m_program );
}


//
GLuint Program::GetProgram() const
{
	return m_program;
}


//
bool Program::SetTexture( const char* uniformName, const Texture2D& tex )
{
	const int texLocation = glGetUniformLocation( m_program, uniformName );
    if( texLocation == -1 )
        return false;

    m_texBinds[ texLocation ] = tex.GetTexture();
    return true;
}


//
bool Program::SetVec4( const char* uniformName, const Vec4& v )
{
	const int location = glGetUniformLocation( m_program, uniformName );
    if( location == -1 )
        return false;

    m_vec4s[ location ] = v;
    return true;
}


//
bool Program::SetIVec4( const char* uniformName, const IVec4& v )
{
	const int location = glGetUniformLocation( m_program, uniformName );
    if( location == -1 )
        return false;

    m_ivec4s[ location ] = v;
    return true;
}


//
bool Program::SetAttribute( const char* attrName, GLint size, GLenum type, GLboolean normalized, GLsizei stride, void* data, int dataSizeInBytes )
{
	GLint attrLocation = glGetAttribLocation( m_program, attrName );
	if( attrLocation == -1 )
		return false;

	auto iter = m_attributes.find( attrLocation );
	if( iter == m_attributes.end() )
		return false;

	VertexAttribute& attr = iter->second;
	glGenBuffers( 1, &attr.buffer );
	glBindBuffer( GL_ARRAY_BUFFER, attr.buffer );
	glBufferData( GL_ARRAY_BUFFER, dataSizeInBytes, data, GL_STATIC_DRAW );
	glBindBuffer( GL_ARRAY_BUFFER, 0 );

	attr.size = size;
	attr.type = type;
	attr.normalized = normalized;
	attr.stride = stride;
	attr.valid = true;
}


//
void Program::BindUniforms() const
{
	int texUnit = 0;
	for( auto iter : m_texBinds )
	{
	    glActiveTexture( GL_TEXTURE0 + texUnit );
	    glBindTexture( GL_TEXTURE_2D, iter.second );
	    glUniform1i( iter.first, texUnit );
	}

	for( auto iter : m_vec4s )
		glUniform4fv( iter.first, 1, ( const GLfloat* )&iter.second );

	for( auto iter : m_ivec4s )
		glUniform4iv( iter.first, 1, ( const GLint* )&iter.second );

	for( auto iter : m_attributes )
	{
		GLint location = iter.first;
		VertexAttribute& attr = iter.second;

		if( !attr.valid )
			continue;

		glBindBuffer( GL_ARRAY_BUFFER, attr.buffer );
		glVertexAttribPointer( location, attr.size, attr.type, attr.normalized, attr.stride, 0 );
		glEnableVertexAttribArray( location );
	}
}