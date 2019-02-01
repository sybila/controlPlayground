import os, sys, re

workspace = os.path.dirname(__file__)

import GMS as GasMixer
import PBR as Bioreactor
import GAS as GasAnalyser

sys.path.append(os.path.join(workspace, '../connection/'))
import connection as SSH

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

types = {"PBR" : Bioreactor.PBR, "GMS" : GasMixer.GMS, "GAS" : GasAnalyser.GAS}

class Particle():
	def __init__(self, user, folder, server):
		self.folder = folder
		self.connection = SSH.SSHconnection(server, user)
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
