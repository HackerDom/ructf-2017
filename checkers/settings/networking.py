#!/usr/bin/env python3

import checker
import socket
import random

def get_bytes(s, length):
	res = s.encode(encoding='ascii')
	if len(res) > length:
		return res[0:length]
	if len(res) < length:
		res += b' ' * (length - len(res))
	return res

def get_section_name(section_name):
	return get_bytes(section_name, 40)

def get_api_key(api_key):
	return get_bytes(api_key, 80)

def get_patch(patch):
	return ('\n' + '\n'.join(''.join(p) for p in patch)).encode(encoding='ascii')


class State:
	def __init__(self, hostname, port=None):
		self.hostname = hostname
		self.port = 1234 if port is None else port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.hostname, self.port))
	def __del__(self):
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()
	def send(self, message):
		try:
			self.socket.sendall(message)
		except ex:
			checker.down(error="can't send data. {}".format(message), exception=ex)
	def recv(self, length):
		buf = bytearray()
		try:
			while len(buf) < length:
				buf += self.socket.recv(length - len(buf))
			return buf
		except:
			checker.down(error="can't recive full data. recived: {}".format(buf), exception=ex)
	def ensure_ok(self):
		status = self.recv(2).decode(encoding='ascii', errors='ignore')
		if status != 'ok':
			checker.corrupt(error="unexpexted status '{}'".format(status))
	def create_section(self, section_name):
		if type(section_name) == str:
			section_name = get_section_name(section_name)
		self.send(b'add-section' + section_name)
		self.ensure_ok()
		return self.recv(80)
	def add_apikey(self, section_name, old_key, new_key):
		if type(section_name) == str:
			section_name = get_section_name(section_name)
		if type(old_key) == str:
			old_key = get_api_key(old_key)
		if type(new_key) == str:
			new_key = get_api_key(new_key)
		self.send(b'add-apikey ' + section_name + old_key + new_key)
		self.ensure_ok()
	def fix_section(self, section_name, apikey, patch):
		if type(section_name) == str:
			section_name = get_section_name(section_name)
		if type(apikey) == str:
			apikey = get_api_key(apikey)
		if type(patch) == list:
			patch = get_patch(patch)
		self.send(b'fix-section' + section_name + apikey + patch)
		self.ensure_ok()
		return self.recv(40)
