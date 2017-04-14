all:
	g++ -g -std=c++11 redbutton.cpp shader.cpp texture.cpp egl.cpp png.cpp glwrap.cpp httpserver.cpp detector.cpp requesthandler.cpp allocator.cpp -lEGL -lGLESv2 -lpng12 -lmicrohttpd -luuid -o redbutton

debug:
	g++ -g -std=c++11 -DDEBUG=1 redbutton.cpp shader.cpp texture.cpp egl.cpp png.cpp glwrap.cpp httpserver.cpp detector.cpp requesthandler.cpp allocator.cpp -lEGL -lGLESv2 -lpng12 -lmicrohttpd -luuid -o redbutton
