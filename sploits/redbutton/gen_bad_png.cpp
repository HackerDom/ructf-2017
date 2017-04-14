#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <zlib.h>
#include <arpa/inet.h>

const char* PNG_HEADER = "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a";
const uint32_t PNG_HEADER_SIZE = 8;

struct IHDR
{	
	const uint32_t length = 0x0d000000;
	const char ihdr[ 4 ] = { 0x49, 0x48, 0x44, 0x52 };
	uint32_t w;
	uint32_t h;
	const uint8_t  bit_depth = 8;
	const uint8_t  color_type = 6;
	const uint8_t  compression = 0;
	const uint8_t  filter_mode = 0;
	const uint8_t  interlace_mode = 0;
};

struct IDAT
{
	uint32_t length;
	const char idat[ 4 ] = { 0x49, 0x44, 0x41, 0x54 };
};

struct IEND
{
	const uint32_t length = 0;
	const char iend[ 4 ] = { 0x49, 0x45, 0x4e, 0x44 };
};

uint32_t CRC32( const uint8_t* data, uint32_t size )
{
	uLong crc = crc32(0L, Z_NULL, 0);
	return crc32( crc, data, size );

}

int main( int argc, const char* argv[] )
{
	if( argc != 4 ){
		printf( "./gen_bad_png <file.png> <w> <h>\n" );
		return 1;
	}
	FILE* f = fopen( argv[ 1 ], "w" );
	fwrite( PNG_HEADER, PNG_HEADER_SIZE, 1, f );

	IHDR ihdr;
	ihdr.w = htonl( atoi( argv[ 2 ] ) );
	ihdr.h = htonl( atoi( argv[ 3 ] ) );
	uint32_t ihdr_crc = htonl( CRC32( ( const uint8_t* )&ihdr.ihdr, 17 ) ); // 17 = "IHDR" + dat
	fwrite( &ihdr, 1, 21, f );
	fwrite( &ihdr_crc, 1, 4, f );

	IDAT idat;
	const uint32_t dummyDataSize = 16;
	uint8_t dummyData[ dummyDataSize ];
	memset( dummyData, 0xde, dummyDataSize );
	idat.length = htonl( dummyDataSize );
	uint32_t idat_crc = htonl( CRC32( ( const uint8_t* )&idat.idat, 4 + dummyDataSize ) ); // 20 = "IDAT" + dummyDataSize
	fwrite( &idat, 1, 8, f );
	fwrite( dummyData, 1, dummyDataSize, f );
	fwrite( &idat_crc, 1, 4, f );

	IEND iend;
	uint32_t iend_crc = htonl( CRC32( ( const uint8_t* )&iend.iend, 4 ) );
	fwrite( &iend, sizeof( IEND ), 1, f );
	fwrite( &iend_crc, 4, 1, f );

	return 0;
}
