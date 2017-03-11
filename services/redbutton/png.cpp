#include "png.h"
#include <png.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void PNGAPI error_function( png_structp png, png_const_charp dummy )
{
  ( void )dummy;
  longjmp( png_jmpbuf( png ), 1 );
}


int read_png( const char* file_name, Image& image )
{
	png_structp png;
	png_infop info;
	int color_type, bit_depth, interlaced;
	int has_alpha;
	int num_passes;
	int p;
	int ok = 0;
	png_uint_32 width, height, y;
	int stride;
	uint8_t* rgb = NULL;

	FILE * fp;

	fp = fopen( file_name, "rb" );
	if( fp == NULL )
		return -1;

	png = png_create_read_struct( PNG_LIBPNG_VER_STRING, 0, 0, 0 );
	if( png == NULL )
		goto End;

	png_set_error_fn( png, 0, error_function, NULL );
	if( setjmp( png_jmpbuf( png ) ) )
	{
		Error:
			png_destroy_read_struct( &png, NULL, NULL );
			free( rgb );
		goto End;
	}

	info = png_create_info_struct( png );
	if ( info == NULL )
		goto Error;

	png_init_io( png, fp );
	png_read_info( png, info );
	if( !png_get_IHDR( png, info, &width, &height, &bit_depth, &color_type, &interlaced, NULL, NULL ) )
		goto Error;

	png_set_strip_16( png );
	png_set_packing( png );
	if( color_type == PNG_COLOR_TYPE_PALETTE )
		png_set_palette_to_rgb( png );
	if( color_type == PNG_COLOR_TYPE_GRAY || color_type == PNG_COLOR_TYPE_GRAY_ALPHA )
	{
		if ( bit_depth < 8 )
			png_set_expand_gray_1_2_4_to_8( png );
		png_set_gray_to_rgb( png );
	}
	if( png_get_valid( png, info, PNG_INFO_tRNS ) )
	{
		png_set_tRNS_to_alpha( png );
		has_alpha = 1;
	}
	else
	{
		has_alpha = !!( color_type & PNG_COLOR_MASK_ALPHA );
	}


	num_passes = png_set_interlace_handling( png );
	png_read_update_info( png, info );
	stride = ( has_alpha ? 4 : 3 ) * width * sizeof( *rgb );
	rgb = ( uint8_t* )malloc( stride * height );
	if( rgb == NULL )
		goto Error;
	for ( p = 0; p < num_passes; ++p )
	{
		for ( y = 0; y < height; ++y )
		{
			png_bytep row = rgb + y * stride;
			png_read_rows( png, &row, NULL, 1 );
		}
	}
	png_read_end( png, info );
	png_destroy_read_struct( &png, &info, NULL );

	image.width = width;
	image.height = height;
	image.rgba = new RGBA[ height * width ];
	for( size_t y = 0; y < height; y++ )
		for( size_t x = 0; x < width; x++ )
		{
			size_t i = y * width + x;
			if ( has_alpha )
			{
				image.rgba[ i ].r = rgb[ stride * y + x * 4 + 1 ];
				image.rgba[ i ].g = rgb[ stride * y + x * 4 + 2 ];
				image.rgba[ i ].b = rgb[ stride * y + x * 4 + 3 ];
			}
			else
			{
				image.rgba[ i ].r = rgb[ stride * y + x * 3 + 0 ];
				image.rgba[ i ].g = rgb[ stride * y + x * 3 + 1 ];
				image.rgba[ i ].b = rgb[ stride * y + x * 3 + 2 ];
			}
		}
	free( rgb );

	End:
		fclose( fp );
		return ok;
}


//
int save_png( const char* file_name, const Image& image )
{
 	/*int i =0;
	uint8_t* rgba = new uint8_t[ image.height * image.width * 4 ];
	for( size_t y = 0; y < image.height; y++ )
		for( size_t x = 0; x < image.width; x++ )
		{
			size_t j = y * image.width + x;
			rgb[i++] = image.image[j].r;
			rgb[i++] = image.image[j].g;
			rgb[i++] = image.image[j].b;
		}*/

	png_structp png;
	png_infop info;
	png_uint_32 y;

	png = png_create_write_struct( PNG_LIBPNG_VER_STRING, NULL, NULL, NULL );
	if( png == NULL )
		return -1;

	info = png_create_info_struct( png );
	if( info == NULL )
	{
		png_destroy_write_struct( &png, NULL );
		return -1;
	}

	if( setjmp( png_jmpbuf( png ) ) )
	{
		png_destroy_write_struct( &png, &info );
		return -1;
	}
	FILE * fp = NULL;

	fp = fopen( file_name, "wb" );
	if( fp == NULL )
	{
		png_destroy_write_struct( &png, &info );
		return -1;
	}
	png_init_io( png, fp );
	png_set_IHDR( png, info, image.width, image.height, 8,
		   PNG_COLOR_TYPE_RGB_ALPHA,
		   PNG_INTERLACE_NONE, PNG_COMPRESSION_TYPE_DEFAULT,
		   PNG_FILTER_TYPE_DEFAULT );
	png_write_info( png, info );
	for ( y = 0; y < image.height; ++y )
	{
		png_bytep row = ( png_bytep )( image.rgba + y * image.width );
		png_write_rows( png, &row, 1 );
	}
	png_write_end( png, info );
	png_destroy_write_struct( &png, &info );
	fclose( fp );
	return 0;
}