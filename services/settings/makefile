.PHONY: all clean c listing clean-all

cblFiles=settings.cbl errnomessage.cbl logerror.cbl logerrorblock.cbl performserverdescriptor.cbl tunesocket.cbl starthandling.cbl processrequest.cbl addsection.cbl fixsection.cbl addapikey.cbl random.cbl getsection.cbl 
cFiles=get_errno.c utils.c polling.c
files=${cblFiles} ${cFiles}

genFiles=$(cblFiles:.cbl=.c) $(cblFiles:.cbl=.c.h) $(cblFiles:.cbl=.c.l.h)
lstFiles=$(cblFiles:.cbl=.lst)

all: settings

settings: ${files}
	cobc -x -O2 -W -g $^

c: ${files}
	cobc -C $^

listing: ${cblFiles}
	cobc -P -fsyntax-only $^

clean:
	-rm ${genFiles}
	-rm ${lstFiles}
	-rm *.so
	-rm *.i

clean-all: clean
	-rm settings
