import threading
import random
import time
import numpy as np
from scipy import interpolate

import bioreactor

class Particle(threading.Thread, bioreactor.Logger):
	def __init__(self, position, step, observer, node, dir_name, cognitive_parameter=0.3, social_parameter=0.5, inertia_weight=0.4):
		threading.Thread.__init__(self)
		self.position = position
		self.step = step

		self.observer = observer
		self.node = node
		self.dir_name = dir_name

		bioreactor.Logger.__init__(self, dir_name, node.PBR.ID)

		self.particle_result = ([], 0)
		self.particle_trace = []

		self.cognitive_parameter = cognitive_parameter
		self.social_parameter = social_parameter
		self.inertia_weight = inertia_weight

		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			self.log("_"*30, "\nI'm computing:\n", list(zip(self.observer.parameter_keys, self.position)))
			result = self.compute_cost_function()
			if self.node.stop_working:
				continue
			self.log("I have computed:", result)
			self.particle_trace.append((self.position, result))
			self.observer.swarm_results.append((self.position, result))
			if result > self.particle_result[1]:
				self.particle_result = (self.position, result)
			self.position = self.next_position()

	# let a bioreactor do its stuff
	def compute_cost_function(self):
		return self.node.stabilise(self.position, self.observer.parameter_keys)

	# decide new position for the bioreactor
	def next_position(self):
		new_position = self.position + self.inertia_weight * self.step + \
					   self.cognitive_parameter * random.random() * (self.particle_result[0] - self.position) + \
					   self.social_parameter * random.random() * (self.observer.swarm_best[0] - self.position)
		return self.check_boundaries(new_position)

	def check_boundaries(self, new_position):
		smaller_than_min = new_position < self.observer.boundaries[0]
		greater_than_max = new_position > self.observer.boundaries[1]
		for i in range(len(smaller_than_min)):
			if smaller_than_min[i]:
				new_position[i] = self.observer.boundaries[0][i]
		for i in range(len(greater_than_max)):
			if greater_than_max[i]:
				new_position[i] = self.observer.boundaries[1][i]
		return new_position

	def join(self, timeout=None):
		super(Particle, self).join(timeout)

	def exit(self):
		self.node.stop_working = True
		self.stoprequest.set()
		self.node.connection.disconnect()
		time.sleep(2)
		self.node.PBR.set_pump_state(5, False)
		self.log("Particle interrupted, bye sweet world!")