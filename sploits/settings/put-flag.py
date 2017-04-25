#!/usr/bin/python

from networking import State

con = State('localhost')
key, section = con.create_section('FlagSection')
con.fix_section('FlagSection', key, [('Flag', '3sS7LPx8QTz3SH6CUbStqgUFqDWvH0G=')])
