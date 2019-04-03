import os, sys, re, time

from .devices import GMS, GAS, PBR
from .connection import SSHconnection
from .stabilisation import get_growth_rate

HEADER = \
'''#!/usr/bin/env gosh

(use util.match)
(use sad.channel3-rv)
(use sad.gauche)
(use srfi-19)
(use sad.rendezvous)
(use sad.binary-channels)
(use util.list)
(use gauche.threads)
(use sad.regression)

'''

types = {"PBR" : PBR, "GMS" : GMS, "GAS" : GAS}

class Node():
	def __init__(self, user='root', folder='/root/control/', server='192.168.17.13'):
		self.folder = folder
		self.connection = SSHconnection(server, user)
		self.devices = []

	def add_device(self, name, ID, adress):
		setattr(self, name, types[name](self, ID, adress))
		self.devices.append(name)

	def write_scm_file(self, device, value, args=[]):
		'''
		Creates a Scheme script by composing HEADER and COMMAND constants with given arguments
		'''
		with open(device.filename, 'w') as file:
			file.write(HEADER)
			file.write(device.definition)
			file.write(device.command[0] + value + " " + " ".join(map(str, args)) + device.command[1])

	def execute(self, device, value, args=[]):
		'''
		Reads output from bioreactor by calling a Scheme script
		'''
		self.write_scm_file(device, value, args)

		self.connection.put(device.filename, self.folder + os.path.basename(device.filename))
		ssh_stdin, ssh_stdout, ssh_stderr = \
				self.connection.execute_cmd("gosh " + self.folder + re.escape(os.path.basename(device.filename)))

		if ssh_stderr.readlines():
			print(ssh_stderr.readlines())
		output = ssh_stdout.readlines()

		return output

	def stabilise(self, conditions, parameter_keys):
		return get_growth_rate(self, conditions, parameter_keys)