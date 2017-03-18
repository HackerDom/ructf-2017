#include <stdio.h>
#include <string.h>
#include "glwrap.h"


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
    Context ctx;
    InitEGL( ctx );

    VertexShader vs( "shaders/simple.vert" );
    FragmentShader fs( "shaders/checkboard.frag" );
    Program pr( vs, fs );
    pr.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );
    pr.SetAttribute( "v_uv", 2, GL_FLOAT, GL_FALSE, 0, vUv, 6 * 2 * sizeof( GLfloat ) );

    /*const int C = 4;
    Texture2D* texture[ C ];
    for( int i = 0; i < C; i++ )
        texture[ i ] = new Texture2D( 2, 2, FORMAT_RGBA );

    for( int i = 0; i < C; i++ )
    {
        pr.SetVec4( "color", Vec4( 1.0f - ( float )i * 0.25f, ( float )i * 0.25f, 0.0f, 1.0f ) );
        BindFramebuffer( *texture[ i ] );
        Clear( 0.0, 0.0, 0.0, 0.0 );

        SetProgram( pr );
        glDrawArrays( GL_TRIANGLES, 0, 6 );

        Image image0;
        ReadPixels( image0 );
        char buf[ 256 ];
        memset( buf, 0, 256 );
        sprintf( buf, "image%d.png", i );
        save_png( buf, image0 );
    }

    for( int i = 0; i < C; i++ )
        delete texture[ i ];

    int W = 4096;
    int H = 4096;
    for( int i = 0; i < C; i++ )
        texture[ i ] = new Texture2D( W, H, FORMAT_RGBA );

    //
    for( int i = 0; i < C; i++ )
    {
        Texture2D target( W, H, FORMAT_RGBA );

        VertexShader vs( "shaders/simple.vert" );
        FragmentShader fs_copy( "shaders/copy.frag" );
        Program pr_copy( vs, fs_copy );
        pr_copy.SetTexture( "tex", *texture[ i ] );
        pr_copy.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );
        pr_copy.SetAttribute( "v_uv", 2, GL_FLOAT, GL_FALSE, 0, vUv, 6 * 2 * sizeof( GLfloat ) );

        BindFramebuffer( target );
        Clear( 0.0, 0.0, 0.0, 0.0 );

        SetProgram( pr_copy );
        glDrawArrays( GL_TRIANGLES, 0, 6 );

        //
        Image image1;
        ReadPixels( image1 );
        char buf[ 256 ];
        memset( buf, 0, 256 );
        sprintf( buf, "imageX%d.png", i );
        save_png( buf, image1 );

        BindFramebuffer( target );
        Clear( 0.0, 0.0, 0.0, 0.0 );

        BindFramebuffer( *texture[ i ] );
        Clear( 0.0, 0.0, 0.0, 0.0 );
    }

    for( int i = 0; i < C; i++ )
        delete texture[ i ];*/

    /////
    {
        Image cr;
        read_png( "crosses.png", cr );
        Texture2D crTex( cr );

        VertexShader vs( "shaders/simple.vert" );
        FragmentShader fs_flag( "shaders/flag.frag" );
        Program pr_flag( vs, fs_flag );
        pr_flag.SetTexture( "tex", crTex );
        pr_flag.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );

        const int W = 32;
        const int H = 1;
        Texture2D target2x2( W, H, FORMAT_RGBA );

        BindFramebuffer( target2x2 );
        Clear( 0.0, 0.0, 0.0, 0.0 );

        SetProgram( pr_flag ); 
        glDrawArrays( GL_TRIANGLES, 0, 6 );

        //
        Image image2x2;
        ReadPixels( image2x2 );
        save_png( "image2x2.png", image2x2 );

        for( int i = 0; i < W; i++ ) {
            printf( "%u %u %u %u\n", image2x2.rgba[ i ].r, image2x2.rgba[ i ].g, 
            image2x2.rgba[ i ].b, 
            image2x2.rgba[ i ].a );
        }
    }

    ShutdownEGL( ctx );
    return 0;
}
