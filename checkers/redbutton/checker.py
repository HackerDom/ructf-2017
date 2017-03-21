#!/usr/bin/env python3
from __future__ import print_function
from sys import argv, stderr
import os

SERVICE_NAME = "redbutton"
OK, CORRUPT, MUMBLE, DOWN, CHECKER_ERROR = 101, 102, 103, 104, 110


def close(code, public="", private="", minidumpFilePath=""):
	if public:
		print(public)
	if private:
		print(private, file=stderr)
	print('Exit with code %d' % code, file=stderr)
	exit(code)


def check(*args):
	close(OK)


def put(*args):
	addr = args[0]
	flag_id = args[1]
	flag = args[2]

	COLOR_R = 237.0
	COLOR_G = 28.0
	COLOR_B = 36.0
	L0 = 40.0
	L1 = 26.0
	ANGLE = 90.0

	flag_defs = ""
	for i in range( 0, 16 ):
		s = flag[ i * 2 : ]
		byte = int( s[:2], 16 )
		flag_defs = flag_defs + ("-D F%d=%d " % ( i, byte ) )

	output_file = "%s.bin" % flag_id
	defines = "-D COLOR_R=%s -D COLOR_G=%s -D COLOR_B=%s -D L0=%s -D L1=%s -D ANGLE=%s %s" % ( COLOR_R, COLOR_G, COLOR_B, L0, L1, ANGLE, flag_defs )
	driver = "Mali-400_r4p0-00rel1"
	core = "Mali-400"
	rev = "r0p0"
	cmd = "./malisc --fragment -d %s -c %s -r %s %s flag.frag -o %s" % ( driver, core, rev, defines, output_file )
	os.system( cmd )
	output_file_np = output_file + ".non-prerotate"
	output_file_p = output_file + ".prerotate"

	f = open( output_file_np, 'rb' )
	shader_binary = f.read()
	# TODO send binary

	os.remove( output_file_np )
	os.remove( output_file_p )
	

def get(*args):
	addr = args[0]
	flag_id = args[1]
	flag = args[2]


def info(*args):
    close(OK, "vulns: 1")


COMMANDS = {'check': check, 'put': put, 'get': get, 'info': info}


def not_found(*args):
    print("Unsupported command %s" % argv[1], file=stderr)
    return CHECKER_ERROR


if __name__ == '__main__':
	try:
		COMMANDS.get(argv[1], not_found)(*argv[2:])
	except Exception as e:
		close(CHECKER_ERROR, "Evil checker", "INTERNAL ERROR: %s" % e)
