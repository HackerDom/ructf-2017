#include <stdio.h>
#include <string.h>
#include "glwrap.h"
#include "allocator.h"
#include "httpserver.h"
#include "requesthandler.h"


static GLfloat vVertices[] = {  -1.0f,  1.0f, 0.0f,
                                 1.0f,  1.0f, 0.0f,
                                 1.0f, -1.0f, 0.0f,
                                -1.0f,  1.0f, 0.0f,
                                 1.0f, -1.0f, 0.0f,
                                -1.0f, -1.0f, 0.0f };

GLfloat vUv[] = {   0.0f, 1.0f,
                    1.0f, 1.0f,
                    1.0f, 0.0f,
                    0.0f, 1.0f,
                    1.0f, 0.0f,
                    0.0f, 0.0f
};

//
int main(int argc, char *argv[])
{
    InitAllocator();
    InitEGL();
#if 1
	TemplateStorage templates("templates");
	DetectorStorage detectors("detectors");

	RequestHandler handler(&detectors, &templates);
	HttpServer server(&handler);

	server.Start(16780);

	while(1){
        sleep(1);
    }

	server.Stop();
#endif

#if 0
    /////
    {
        Image cr;
        read_png( argv[ 1 ], cr );
        Texture2D crTex( cr );

        VertexShader vs( "shaders/simple.vert", false );
        FragmentShader fs( "shaders/flag.frag", false );
        
        Program pr_flag( vs, fs );
        pr_flag.SetTexture( "tex", crTex );
        pr_flag.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );

        const int W = 4;
        const int H = 1;
        Texture2D target( W, H, FORMAT_RGBA );

        BindFramebuffer( target );
        Clear( 0.0, 0.0, 0.0, 0.0 );

        SetProgram( pr_flag ); 
        glDrawArrays( GL_TRIANGLES, 0, 6 );

        //
        Image flagImage;
        ReadPixels( flagImage );
        save_png( "flag.png", flagImage );

        for( int i = 0; i < W; i++ ) {
            printf( "%u %u %u %u\n", flagImage.rgba[ i ].r, flagImage.rgba[ i ].g, 
            flagImage.rgba[ i ].b, 
            flagImage.rgba[ i ].a );
        }
        uint8_t* bytes = ( uint8_t* )flagImage.rgba;
        for( int i = 0; i < W * 4; i++ ){
            printf( "%02X", bytes[ i ] );
        }
        printf( "\n" );
    }
#endif

#if 0
    {
        FILE* f = fopen( "crosses.png", "r" );
        fseek( f, 0, SEEK_END );
        size_t fileSize = ftell( f );
        fseek( f, 0, SEEK_SET );
        char* fileData = new char[ fileSize ];
        memset( fileData, 0, fileSize );
        fread( fileData, 1, fileSize, f );
        fclose( f );

        Texture2D source( fileData, fileSize );
        Texture2D target( source.GetWidth(), source.GetHeight(), FORMAT_RGBA );

        VertexShader vs( "shaders/simple.vert", false );
        FragmentShader fs_copy( "shaders/copy.frag", false );
        Program pr_copy( vs, fs_copy );
        pr_copy.SetTexture( "tex", source );
        pr_copy.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );
        pr_copy.SetAttribute( "v_uv", 2, GL_FLOAT, GL_FALSE, 0, vUv, 6 * 2 * sizeof( GLfloat ) );

        //
        BindFramebuffer( target );
        Clear( 0.0, 0.0, 0.0, 0.0 );
        SetProgram( pr_copy );
        glDrawArrays( GL_TRIANGLES, 0, 6 );

        //
        RGBA* rgba = nullptr;
        target.ReadBack( rgba );
        save_png( "copy_test.png", rgba, target.GetWidth(), target.GetHeight() );
    }
#endif

#if 0
    {
        FILE* f = fopen( "../../sploits/redbutton/test.png", "r" );
        fseek( f, 0, SEEK_END );
        size_t fileSize = ftell( f );
        fseek( f, 0, SEEK_SET );
        char* fileData = new char[ fileSize ];
        memset( fileData, 0, fileSize );
        fread( fileData, 1, fileSize, f );
        fclose( f );

        Texture2D test( fileData, fileSize );
    }
#endif

    ShutdownEGL();
    return 0;
}
