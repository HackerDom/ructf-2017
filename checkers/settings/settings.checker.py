#!/usr/bin/env python3

import sys
from checker import Checker
import checker
from networking import State
import random
import json

def get_patch():
	return [[' ' if random.randint(0, 2) != 0 else '*' for i in range(80)] for j in range(8)]

def handler_check(hostname):

	soc1 = State(hostname)
	soc2 = State(hostname)
	for i in range(2):
		section_name = checker.get_rand_string(40)
		key1 = soc1.create_section(section_name)
		key2 = checker.get_rand_string(80)
		soc1.add_apikey(section_name, key1, key2)
		soc1.fix_section(section_name, key1, get_patch())
		soc1.fix_section(section_name, key2, get_patch())
	
		key3 = checker.get_rand_string(80)
		soc2.add_apikey(section_name, key2, key3)
		soc2.fix_section(section_name, key3, get_patch())

	checker.ok()

def handler_get(hostname, id, flag):
	id = json.loads(id)
	section_name = id['section_name']
	key = id['key']
	con = State(hostname)
	con.fix_section(section_name, key, get_patch())
	checker.ok()

def handler_put_1(hostname, id, flag):
	con = State(hostname)
	key = con.create_section(flag)
	checker.ok(message=json.dump({'key': key, 'section_name': flag}))

def handler_put_2(hostname, id, flag):
	con = State(hostname)
	section_name = checker.get_rand_string(40)
	key = con.create_section(section_name)
	con.add_apikey(section_name, key, flag)
	checker.ok(message=json.dump({'key': flag, 'section_name': section_name}))

def main():
	checker = Checker(handler_check, [(handler_put_1, handler_get), (handler_put_2, handler_get)])
	checker.process(sys.argv)

if __name__ == "__main__":
	main()
