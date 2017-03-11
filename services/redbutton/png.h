#pragma once
#include <stdint.h>


//
union RGBA
{
	struct
	{
		uint32_t r : 8;
		uint32_t g : 8;
		uint32_t b : 8;
		uint32_t a : 8;
	};
	uint32_t rgba;
};


//
struct Image
{
    RGBA*		rgba;
    uint16_t 	width;
    uint16_t 	height;

    Image()
    	: rgba( nullptr ), width( 0 ), height( 0 )
    {

    }

    Image( uint16_t w, uint16_t h )
    	: rgba( nullptr ), width( w ), height( h )
    {
    	rgba = new RGBA[ w * h ];
    }

    Image( const Image& ) = delete;
    Image( const Image&& ) = delete;
    Image& operator=( const Image&& ) = delete;

    ~Image()
    {
        if( rgba )
            delete[] rgba;
    }
};


//
int read_png( const char* file_name, Image& image );
int save_png( const char* file_name, const Image& image );
uint8_t* ALPHA( const uint32_t & argb );
uint8_t* RED( const uint32_t & argb );
uint8_t* GREEN( const uint32_t & argb );
uint8_t* BLUE( const uint32_t & argb );