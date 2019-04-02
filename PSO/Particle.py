import threading
import random
import time
import numpy as np
from scipy import interpolate

# this is basically the Particle
class Particle(threading.Thread):
	def __init__(self, position, step, results, observer, node, cognitive_parameter=0.3, social_parameter=0.5, inertia_weight=0.4):
		super(Particle, self).__init__()
		self.position = position
		self.step = step

		self.swarm_results = results
		self.observer = observer

		self.node = node

		self.particle_result = ([], 0)
		self.particle_trace = []

		self.cognitive_parameter = cognitive_parameter
		self.social_parameter = social_parameter
		self.inertia_weight = inertia_weight

		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			print(self.name, "I'm computing:", self.position)
			result = self.compute_cost_function()
			print(self.name, "I have computed:", result)
			self.particle_trace.append((self.position, result))
			self.swarm_results.append((self.position, result))
			if result > self.particle_result[1]:
				self.particle_result = (self.position, result)
			self.position = self.next_position()

	# let a bioreactor do its stuff
	def compute_cost_function(self):
		#return self.node.stabilise(self.position)
		return f(*self.position)

	# decide new position for the bioreactor
	def next_position(self):
		new_position = self.position + self.inertia_weight * self.step + \
					   self.cognitive_parameter * random.random() * (self.particle_result[0] - self.position) + \
					   self.social_parameter * random.random() * (self.observer.swarm_best[0] - self.position)

		# new_position in boundaries?
		return new_position

	def join(self, timeout=None):
		# self.stoprequest.set()
		super(Particle, self).join(timeout)

temperature = (20,25,30,35,40)
lights = (100,200,400,800)
growth_rates = ((1.5,2,2.1,2,1),(1.7,0.8,2.3,2.1,1.2),(1.8,1.4,2.9,2.2,1.3),(1.6,2.1,2.2,2,1.1))
f = interpolate.interp2d(temperature, lights, growth_rates, kind='linear')