.PHONY: all clean c listing clean-all

cblFiles=settings.cbl errnomessage.cbl logerror.cbl logerrorblock.cbl performserverdescriptor.cbl tunesocket.cbl starthandling.cbl processrequest.cbl addsection.cbl fixsection.cbl addapikey.cbl random.cbl getsection.cbl allsection.cbl runcommand.cbl
cpyFiles=sectiondb.cpy sectionrecord.cpy settingdb.cpy settingrecord.cpy
cFiles=get_errno.c utils.c polling.c

compiledFiles=${cblFiles} ${cFiles}
files=${cblFiles} ${cFiles} ${cpyFiles}

genFiles=$(cblFiles:.cbl=.c) $(cblFiles:.cbl=.c.h) $(cblFiles:.cbl=.c.l.h)
lstFiles=$(cblFiles:.cbl=.lst) $(cpyFiles:.cpy=.lst)

all: settings

settings: ${files}
	cobc -x -O2 -W -g ${compiledFiles}

c: ${files}
	cobc -C ${compiledFiles}

listing: ${cblFiles} ${cpyFiles}
	cobc -P -fsyntax-only ${cpyFiles}

clean:
	-rm ${genFiles}
	-rm ${lstFiles}
	-rm *.so
	-rm *.i

clean-all: clean
	-rm settings
	-rm *.dat
