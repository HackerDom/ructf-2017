#include <stdio.h>
#include <string.h>
#include <GLES2/gl2.h>
#include "egl.h"
#include "shader.h"
#include "texture.h"
#include "png.h"

#include "detector.h"


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
	/*TestHandler handler;
	HttpServer server(&handler);

	server.Start(16780);

	getchar();

	server.Stop();*/

	/*TemplateStorage templates("templates");

	printf("%s\n", templates.GetTemplate("test")->Fill("hello", "Hello, world!", "footer", "-- footer --"));*/

	DetectorStorage storage("detectors");

	for (int i = 0; i < 5; i++)
	{
		uuid id;
		uuid_generate(id.bytes);

		char buffer[256];
		uuid_unparse(id.bytes, buffer);

		printf("%s\n", buffer);

		char data[256];
		sprintf(data, "Test Data %d", i);

		storage.AddDetector(id, data, strlen(data) + 1);
	}

	int idCount;
	uuid *ids = storage.ListDetectors(&idCount);

	printf("---\n");

	for (int i = 0; i < idCount; i++)
	{
		char buffer[256];
		uuid_unparse(ids[i].bytes, buffer);

		printf("%s = %s\n", buffer, storage.GetDetector(ids[i])->data);
		//printf("%s = ??\n", buffer);
	}

	return 0;


    Context ctx;
    InitEGL( ctx );

    const char* attribList[] = { "v_pos" };
    VertexShader vs( "shaders/simple.vert" );
    FragmentShader fs( "shaders/simple.frag" );
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

    /////
    FragmentShader fs_flag( "shaders/flag.frag" );
    Program pr_flag( vs, fs_flag, attribList, 1 );

    Texture2D target2x2( 2, 2, FORMAT_RGBA );

    glBindFramebuffer( GL_FRAMEBUFFER, target2x2.GetFramebuffer() );
    glClearColor( 0.0, 0.0, 0.0, 0.0 );
    glViewport(0, 0, 2, 2 );
    glClear( GL_COLOR_BUFFER_BIT );

    glUseProgram( pr_flag.GetProgram() );

    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, vVertices );
    glEnableVertexAttribArray( 0 );
    glDrawArrays( GL_TRIANGLES, 0, 6 );

    //
    glPixelStorei(GL_PACK_ALIGNMENT, 1);
    Image image2x2( 2, 2 );
    glReadPixels(0, 0, 2, 2, GL_RGBA, GL_UNSIGNED_BYTE, ( GLvoid* )image2x2.rgba );
    CheckError( "glReadPixels");
    save_png( "image2x2.png", image2x2 );
    
    ShutdownEGL( ctx );
    return 0;
}
