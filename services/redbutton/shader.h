#pragma once


//
class Shader
{
public:
	//
	Shader() = delete;
	Shader( GLuint type, const char* fileName );
	~Shader();

	GLuint GetShader() const;
	bool IsValid() const;

private:
	//
	GLuint m_shader = 0;	
};


//
class VertexShader : public Shader
{
public:
	VertexShader() = delete;
	VertexShader( const char* fileName );
};


//
class FragmentShader : public Shader
{
public:
	FragmentShader() = delete;
	FragmentShader( const char* fileName );
};


//
class Program
{
public:
	//
	Program() = delete;
	Program( const VertexShader& vs, const FragmentShader& fs, const char** attributeList, int attributesNum );

	GLuint GetProgram() const;

private:
	//
	const VertexShader& 	m_vs;
	const FragmentShader& 	m_fs;
	GLuint 					m_program = 0;
};