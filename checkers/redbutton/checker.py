#!/usr/bin/env python3
from __future__ import print_function
from sys import argv, stderr
import os
import requests
import UserAgents
import json
import stars
import random

SERVICE_NAME = "redbutton"
OK, CORRUPT, MUMBLE, DOWN, CHECKER_ERROR = 101, 102, 103, 104, 110


WIDTH = 128
HEIGHT = 128


def close(code, public="", private=""):
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

	COLOR_R = int( random.random() * 255 )
	COLOR_G = int( random.random() * 255 )
	COLOR_B = int( random.random() * 255 )
	L0 = random.uniform( 10.0, 50.0 )
	L1 = random.uniform( 10.0, 50.0 )
	ANGLE = random.uniform( 30.0, 90.0 )

	flag_defs = ""
	for i in range( len( flag ) ):
		s = flag[ i : ]
		byte = ord( s[:1] )
		flag_defs = flag_defs + ("-D F%d=%d " % ( i, byte ) )
	
	output_file = "/tmp/%s.bin" % flag_id
	defines = "-D COLOR_R=%s -D COLOR_G=%s -D COLOR_B=%s -D L0=%s -D L1=%s -D ANGLE=%s -D WIDTH=%s -D HEIGHT=%s %s" % ( COLOR_R, COLOR_G, COLOR_B, L0, L1, ANGLE, WIDTH, HEIGHT, flag_defs )
	driver = "Mali-400_r4p0-00rel1"
	core = "Mali-400"
	rev = "r0p0"
	cmd = "./malisc --fragment -d %s -c %s -r %s %s flag.frag -o %s > /dev/null 2> /dev/null" % ( driver, core, rev, defines, output_file )
	os.system( cmd )

	os.remove( output_file + ".prerotate" )

	binary_file = output_file + ".non-prerotate"
	
	flag_id = "" # reset flag id, we will build new, based on service response
	url = 'http://%s/detectors/add' % addr
	files = { 'detector': open( binary_file, 'rb' ).read() }
	headers = { 'User-Agent' : UserAgents.get() }
	try:
		r = requests.post(url, files=files, headers=headers )
		if r.status_code == 502:
			close(DOWN, "Service is down", "Nginx 502")
		if r.status_code != 200:
			close( MUMBLE, "Submit error", "Invalid status code: %s %d" % ( url, r.status_code ) )	

		try:
			flag_id = json.dumps( { 'guid' : r.text[:-1], 'COLOR_R' : COLOR_R, 'COLOR_G' : COLOR_G, 'COLOR_B' : COLOR_B, 'L0' : L0, 'L1' : L1, 'ANGLE' : ANGLE } )
		except Exception as e:
			close(CORRUPT, "Service corrupted", "Service returns invalid guid: %s" % e)			
	except Exception as e:
		 close(DOWN, "HTTP Error", "HTTP error: %s" % e)
	close(OK, flag_id)

	os.remove( binary_file )
	

def get(*args):
	addr = args[0]
	flag_id = args[1]
	flag = args[2]
	
	params = json.loads( flag_id )

	guid = params[ 'guid' ]
	COLOR_R = params[ 'COLOR_R' ]
	COLOR_G = params[ 'COLOR_G' ]
	COLOR_B = params[ 'COLOR_B' ]
	COLOR = ( COLOR_R, COLOR_G, COLOR_B, 0xff)
	L0 = params[ 'L0' ]
	L1 = params[ 'L1' ]
	ANGLE = params[ 'ANGLE' ]

	image = stars.generate_image( WIDTH, HEIGHT, COLOR, L0, L1, ANGLE, 5 )

	url = 'http://%s/detectors/%s/check' % ( addr, guid )
	try:
		headers = { 'User-Agent' : UserAgents.get() }
		files = { 'image' : image }
		r = requests.post( url, files=files, headers=headers )
		if r.status_code == 502:
			close(DOWN, "Service is down", "Nginx 502")
		if r.status_code != 200:
			close( MUMBLE, "Invalid HTTP response", "Invalid status code: %s %d" % ( url, r.status_code ) )	
	except Exception as e:
		 close(DOWN, "HTTP Error", "HTTP error: %s" % e)

	print( r.text )


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
