#!/usr/bin/env python3

import sys
from checker import Checker
import checker
from networking import State
import networking
import random
import json

def get_random_key(words):
	key = ''
	for i in range(random.randint(1, 3)):
		key += random.choice(words).rstrip().title()
	return key

def get_random_patch(words):
	res = []
	for i in range(random.randint(1, 7)):
		res.append((get_random_key(words), checker.get_rand_string(87)))
	return res

def add(d1, d2):
	for k, v in d2:
		d1[k] = v

def dicts_diff(d1, d2):
	for k, v in d1.items():
		if k not in d2:
			return "element {} present in first dict, but not in second".format(k)
		if v != d2[k]:
			return "elements for key {} are different: {} vs {}".format(k, v, d2[k])
	for k, v in d2.items():
		if k not in d1:
			return "element {} present in second dict, but not in first".format(k)
		if v != d1[k]:
			return "elements for key {} are different: {} vs {}".format(k, d1[k], v)
	return None

def handler_check(hostname):

	with open('words.txt') as f:
		words = f.readlines()

	for i in range(2):
		section_name = checker.get_rand_string(20)

		soc1 = State(hostname)
		key1, section_name = soc1.create_section(section_name)

		key2 = checker.get_rand_string(40)
		soc1.add_apikey(section_name, key1, key2)
		patches = {}
		add(patches, soc1.fix_section(section_name, key1, get_random_patch(words)))
		add(patches, soc1.fix_section(section_name, key2, get_random_patch(words)))

		soc2 = State(hostname)
		key3 = checker.get_rand_string(40)
		soc2.add_apikey(section_name, key2, key3)
		add(patches, soc2.fix_section(section_name, key3, get_random_patch(words)))
		values = soc1.get_full_section(section_name, key3)

		diff = dicts_diff(patches, values)
		if diff is not None:
			checker.mumble(error="patches are not equal to stored values: {}".format(diff))

		soc3 = State(hostname)
		sections = soc3.get_all_sections()
		if section_name not in sections:
			checker.mumble(error="not found created section. {}".format(section_name))

	checker.ok()

def handler_put(hostname, id, flag):

	with open('words.txt') as f:
		words = f.readlines()

	con = State(hostname)
	section_name = checker.get_rand_string(20)
	apikey, section_name = con.create_section(section_name)
	key = get_random_key(words)
	patch = con.fix_section(section_name, apikey, [(key, flag)])
	key = patch[0][0]
	checker.ok(message=json.dumps({'key': apikey.decode(encoding='ascii', errors='ignore'), 'section_name': section_name.decode(encoding='ascii', errors='ignore'), 'pkey': key.decode(encoding='ascii', errors='ignore')}))

def handler_get(hostname, id, flag):
	id = json.loads(id)
	section_name = id['section_name']
	key = id['key']
	pkey = id['pkey']
	con = State(hostname)
	key = networking.get_api_key(key)
	pkey = networking.get_k(pkey)
	flag = networking.get_v(flag)
	values = con.get_full_section(section_name, key)
	if pkey not in values or values[pkey] != flag:
		checker.corrupt(error='flag not found')
	checker.ok()


def main():
	checker = Checker(handler_check, [(handler_put, handler_get)])
	checker.process(sys.argv)

if __name__ == "__main__":
	main()
