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

def get_method(method):
	return get_bytes(method, 11)

def get_section_name(section_name):
	return get_bytes(section_name, 20)

def get_api_key(api_key):
	return get_bytes(api_key, 40)

def get_start(start):
	return get_bytes(stary, 85)

def get_patch_bytes(patch):
	res = str(len(patch)).encode(encoding='ascii')
	for k, v in patch:
		res += k + v
	return res

def get_patch(patch):
	res = []
	for k, v in patch:
		res.append((get_bytes(k, 20), get_bytes(v, 85)))
	return res

class State:
	def __init__(self, hostname, port=None):
		self.hostname = hostname
		self.port = 12345 if port is None else port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.hostname, self.port))
	def __del__(self):
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()
	def send(self, method, message):
		try:
			if type(method) is str:
				method = get_method(method)
			self.socket.sendall(method + message)
		except Exception as ex:
			checker.down(error="can't send data. {}".format(message), exception=ex)
	def recv(self, length):
		buf = bytearray()
		try:
			while len(buf) < length:
				buf += self.socket.recv(length - len(buf))
			return buf
		except Exception as ex:
			checker.down(error="can't recive full data. recived: {}".format(buf), exception=ex)
	def ensure_ok(self, method):
		status = self.recv(2).decode(encoding='ascii', errors='ignore')
		if status != 'ok':
			checker.corrupt(error="unexpexted status '{}' while {}".format(status, method))
	def send_checked(self, method, message):
		self.send(method, message)
		self.ensure_ok(method)
	def create_section(self, section_name):
		if type(section_name) == str:
			section_name = get_section_name(section_name)
		self.send_checked('add-section', section_name)
		return (self.recv(40), section_name)
	def add_apikey(self, section_name, old_key, new_key):
		if type(section_name) == str:
			section_name = get_section_name(section_name)
		if type(old_key) == str:
			old_key = get_api_key(old_key)
		if type(new_key) == str:
			new_key = get_api_key(new_key)
		self.send_checked('add-apikey', section_name + old_key + new_key)
	def fix_section(self, section_name, apikey, patch):
		if type(section_name) == str:
			section_name = get_section_name(section_name)
		if type(apikey) == str:
			apikey = get_api_key(apikey)
		patch = get_patch(patch)
		self.send_checked('fix-section', section_name + apikey + get_patch_bytes(patch))
		return patch
	def recv_pair(self):
		key = self.recv(20)
		value = self.recv(85)
		return (key, value)
	def get_section(self, section_name, apikey, start=None):
		if type(section_name) == str:
			section_name = get_section_name(section_name)
		if type(apikey) == str:
			apikey = get_api_key(apikey)
		if start is None:
			start = bytes([0] * 85)
		if type(start) == str:
			start = get_bytes(start, 85)
		self.send_checked('get-section', section_name + apikey + start)
		res_length = self.recv(1).decode(encoding='ascii')
		if not res_length.isdigit():
			checker.mumble(error="count is not digit '{}'".format(res_length))
		res = []
		for i in range(int(res_length)):
			el = self.recv_pair()
			res.append(el)
		return res
	def get_full_section(self, section_name, apikey):
		res = {}
		r = self.get_section(section_name, apikey)
		while len(r) > 0:
			for k, v in r:
				res[bytes(k)] = v
			r = self.get_section(section_name, apikey, r[-1][0])
		return res
	def get_sections(self, section_name=None):
		if section_name is None:
			section_name = bytes([0] * 20)
		if type(section_name) == str:
			section_name = get_section_name(section_name)
		self.send_checked('all-section', section_name)
		res_length = self.recv(2).decode(encoding='ascii')
		if not res_length.isdigit():
			checker.mumble(error="count is not digit '{}'".format(res_length))
		res = []
		for i in range(int(res_length)):
			res.append(self.recv(20))
		return res
	def get_all_sections(self):
		res = []
		r = self.get_sections()
		while len(r) > 0:
			res += r
			r = self.get_sections(r[-1])
		return res
