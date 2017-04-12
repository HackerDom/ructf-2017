.PHONY: all clean c listing clean-all

cblFiles=echoserver.cbl errnomessage.cbl logerror.cbl logerrorblock.cbl performserverdescriptor.cbl tunesocket.cbl starthandling.cbl processrequest.cbl
cFiles=get_errno.c utils.c polling.c
files=${cblFiles} ${cFiles}

genFiles=$(cblFiles:.cbl=.c) $(cblFiles:.cbl=.c.h) $(cblFiles:.cbl=.c.l.h)
lstFiles=$(cblFiles:.cbl=.lst)

all: echoserver

echoserver: ${files}
	cobc -x -O2 -W -std=cobol2002 -g $^

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
	-rm echoserver
