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

    {
        VertexShader vs( "shaders/simple.vert" );
        FragmentShader fs( "shaders/simple.frag" );
        Program pr( vs, fs );
        pr.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );
        pr.SetAttribute( "v_uv", 2, GL_FLOAT, GL_FALSE, 0, vUv, 6 * 2 * sizeof( GLfloat ) );

        //
        Texture2D* texture = new Texture2D( 4, 4, FORMAT_RGBA );

        BindFramebuffer( *texture );
        Clear( 0.0, 0.0, 0.0, 0.0 );

        SetProgram( pr );
        glDrawArrays( GL_TRIANGLES, 0, 6 );

        Image image0;
        ReadPixels( image0 );
        save_png( "image0.png", image0 );
        delete texture;
    }

    //
    {
        Texture2D texture( 4, 4, FORMAT_RGBA );
        Texture2D target( 4, 4, FORMAT_RGBA );

        VertexShader vs( "shaders/simple.vert" );
        FragmentShader fs_copy( "shaders/copy.frag" );
        Program pr_copy( vs, fs_copy );
        pr_copy.SetTexture( "tex", texture );
        pr_copy.SetAttribute( "v_pos", 3, GL_FLOAT, GL_FALSE, 0, vVertices, 6 * 3 * sizeof( GLfloat ) );
        pr_copy.SetAttribute( "v_uv", 2, GL_FLOAT, GL_FALSE, 0, vUv, 6 * 2 * sizeof( GLfloat ) );

        BindFramebuffer( target );
        Clear( 0.0, 0.0, 0.0, 0.0 );

        SetProgram( pr_copy );
        glDrawArrays( GL_TRIANGLES, 0, 6 );

        //
        Image image1;
        ReadPixels( image1 );
        save_png( "image1.png", image1 );
    }

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

        const int W = 1;
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
    }

    ShutdownEGL( ctx );
    return 0;
}
