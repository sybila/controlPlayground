import os, sys, re, time

workspace = os.path.dirname(__file__)

import devices.GMS as GasMixer
import devices.PBR as Bioreactor
import devices.GAS as GasAnalyser

sys.path.append(os.path.join(workspace, 'connection/'))
import connection as SSH
sys.path.append(os.path.join(workspace, 'stabilisation/'))
import DataHolder as DH
import GrowthChecker as GC
import Regression

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

class Node():
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

	# this is a method called by a particle, provides growth rate for given conditions
	def get_growth_rate(self, conditions):
		OD_MAX = 0.525
		OD_MIN = 0.475
		TIMEOUT = 10
		# set initial conditions
		set_up_conditions(conditions)
		checker = GC.GrowthChecker(0.01)
		holder = DH.DataHolder(self.PBR, time.time())
		#should return True if not stabilised
		while checker.is_stable(6):
			checker.values.append(reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT))
			checker.times.append(holder.init_time - time.time())
			pump_out_population(holder, OD_MIN, pump, TIMEOUT)
		return checker.values[-1] #which should be stable

	# turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
	def pump_out_population(self, holder, OD_MIN, pump, TIMEOUT):
		self.PBR.set_pump_state(pump, True)
		while holder.next_value() > OD_MIN: # or make a better condition with some tolerance
			time.wait(TIMEOUT)
		self.PBR.set_pump_state(pump, False)
		return True

	# given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
	# calculates current growth rate using measured OD data and exponentional regression
	# has to remember initial OD!
	def reach_max_population(self, holder, OD_MIN, OD_MAX, TIMEOUT):
		initial = len(holder.data)
		while holder.next_value() < OD_MAX: # or make a better condition with some tolerance
			time.wait(TIMEOUT)
		return Regression.exponentional_regression(holder.times, holder.data, holder.data[initial])

	# it is called when we start with new conditions
	# and they are all set for given node
	# assume conditions has form [temp, co2-flow, [channel, intensity]]
	def set_up_conditions(self, conditions):
		T = self.PBR.set_temp[conditions[0]]
		F = self.GAS.set_flow_target(conditions[1])
		L = self.PBR.set_light_intensity(*conditions[2])
		return (T and F and L)
