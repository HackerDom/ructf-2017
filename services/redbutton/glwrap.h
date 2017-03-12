#pragma once
#include <GLES2/gl2.h>
#include <stdint.h>
#include "vec.h"
#include "egl.h"
#include "png.h"
#include "texture.h"
#include "shader.h"


//
void SetProgram( const Program& p );
void BindFramebuffer( const Texture2D& t );
void Clear( float r, float g, float b, float a );
void ReadPixels( Image& i );