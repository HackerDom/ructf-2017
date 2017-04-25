#!/usr/bin/python

from networking import State

con = State('localhost')
pairs = con.get_full_section('FlagSection', '*' * 40)

for k, v in pairs.items():
	print('{} = {}'.format(k.decode(encoding='ascii'), v.decode(encoding='ascii')))
