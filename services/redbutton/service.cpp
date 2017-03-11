#include <stdio.h>
#include <string.h>
#include <GLES2/gl2.h>
#include "egl.h"
#include "shader.h"
#include "texture.h"
#include "png.h"


static GLfloat vVertices[] = {  -1.0f,  1.0f, 0.0f,
                                 1.0f,  1.0f, 0.0f,
                                 1.0f, -1.0f, 0.0f,
                                -1.0f,  1.0f, 0.0f,
                                 1.0f, -1.0f, 0.0f,
                                -1.0f, -1.0f, 0.0f };

/*GLfloat vUv[] = {   0.0f, 0.0f,
                    1.0f, 0.0f,
                    1.0f, 1.0f,
                    0.0f, 0.0f,
                    1.0f, 1.0f,
                    0.0f, 1.0f
};*/

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
    FragmentShader fs( "shaders/simple.frag" );
    const char* attribList[] = { "v_pos" };
    Program pr( vs, fs, attribList, 1 );

    //
    FragmentShader fs_copy( "shaders/copy.frag" );
    Program pr_copy( vs, fs_copy, attribList, 1 );
    const int texLocation = glGetUniformLocation( pr_copy.GetProgram(), "tex" );
    if( texLocation == -1 )
        printf( "dsfds\n");

    //
    Texture2D* texture = new Texture2D( 4, 4, FORMAT_RGBA );

    glBindFramebuffer( GL_FRAMEBUFFER, texture->GetFramebuffer() );
    glClearColor( 0.0, 0.0, 0.0, 0.0 );
    glViewport(0, 0, 4, 4 );
    glClear( GL_COLOR_BUFFER_BIT );

    glUseProgram( pr.GetProgram() );
    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, vVertices );
    glEnableVertexAttribArray( 0 );
    glVertexAttribPointer( 1, 2, GL_FLOAT, GL_FALSE, 0, vUv );
    glEnableVertexAttribArray( 1 );
    glDrawArrays( GL_TRIANGLES, 0, 6 );

    glPixelStorei(GL_PACK_ALIGNMENT, 1);
    Image image0( 4, 4 );
    glReadPixels(0, 0, 4, 4, GL_RGBA, GL_UNSIGNED_BYTE, ( GLvoid* )image0.rgba );
    CheckError( "glReadPixels");
    save_png( "image0.png", image0 );
    delete texture;

    //
    texture = new Texture2D( 4, 4, FORMAT_RGBA );
    Texture2D target( 4, 4, FORMAT_RGBA );

    glBindFramebuffer( GL_FRAMEBUFFER, target.GetFramebuffer() );
    glClearColor( 0.0, 0.0, 0.0, 0.0 );
    glViewport(0, 0, 4, 4 );
    glClear( GL_COLOR_BUFFER_BIT );

    glUseProgram( pr_copy.GetProgram() );

    glActiveTexture( GL_TEXTURE0 );
    glBindTexture( GL_TEXTURE_2D, texture->GetTexture() );
    glUniform1i( texLocation, 0 );

    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, vVertices );
    glEnableVertexAttribArray( 0 );
    glVertexAttribPointer( 1, 2, GL_FLOAT, GL_FALSE, 0, vUv );
    glEnableVertexAttribArray( 1 );
    glDrawArrays( GL_TRIANGLES, 0, 6 );

    //
    glPixelStorei(GL_PACK_ALIGNMENT, 1);
    Image image1( 4, 4 );
    glReadPixels(0, 0, 4, 4, GL_RGBA, GL_UNSIGNED_BYTE, ( GLvoid* )image1.rgba );
    CheckError( "glReadPixels");
    save_png( "image1.png", image1 );
    
    ShutdownEGL( ctx );
    return 0;
}
