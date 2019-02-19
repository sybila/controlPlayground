import bioreactor
import numpy as np
import random
import time
import matplotlib.pyplot as plt

timeout_in_sec = 300

WAIT_TIME = 30  #... chceme merat kazdych 30 sekund
QUEUE_MAX_LENGTH = 20  # poslednych 20 merani
FREQUENCY_OF_CHECK = 10
TIMEOUT = int(timeout_in_sec/WAIT_TIME)

##################################

# plot results
class MyPlot():
	def __init__(self):
		plt.ion()
		self.x = np.array([])
		self.y = np.array([])

	def get_last_x(self):
		if len(self.x) == 0:
			return 0
		return int(self.x[-1])

	def update(self, data, linear, const):
		original = np.array(data)
		self.y = np.append(self.y, original)
		x_data = np.array(range(len(original)))
		self.x = np.append(self.x - 10, x_data)

		fitted = linear*x_data + const

		plt.plot(self.x, self.y, 'o', label='Original data', markersize=5)
		plt.plot(x_data, fitted, 'r', label='Fitted line')
		plt.draw()
		plt.pause(0.0001)
		plt.clf()

# stores last n measures
class LimitedQueue():
	def __init__(self):
		self.queue = []

	def add(self, value):
		self.queue.append(value)
		self.queue = self.queue[-QUEUE_MAX_LENGTH:]

# computes regression
def calculate_regression(data):
	x = np.array(range(len(data)))
	y = np.array(data)
	A = np.vstack([x, np.ones(len(x))]).T
	linear_coeff, const_coeff = np.linalg.lstsq(A, y, rcond=None)[0]
	return linear_coeff, const_coeff

# perform measures for given time
def measure_values(last_values, duration):
	for _ in range(duration):
		time.sleep(WAIT_TIME)
		last_values.add(bioreactor.node.PBR.get_ph())
	return last_values

def reset(linear_coeff_max):
	bioreactor.node.GAS.set_flow_target(0.250) 

	optimised = False
	last_values = LimitedQueue()
	my_plot = MyPlot()

	while not optimised:
		last_values = measure_values(last_values, FREQUENCY_OF_CHECK)

		print("Check with flow ON: ", last_values.queue)
		linear_coeff, const_coeff = calculate_regression(last_values.queue)
		print("Linear coefficient: ", linear_coeff, "\n")
		my_plot.update(last_values.queue, linear_coeff, const_coeff)

		if linear_coeff_max > abs(linear_coeff):
			print("Flow turned off", "\n")
			bioreactor.node.GAS.set_flow_target(0)
			last_values = measure_values(last_values, TIMEOUT)
			print("Check with flow OFF: ", last_values.queue)
			linear_coeff, const_coeff = calculate_regression(last_values.queue)
			print("Linear coefficient: ", linear_coeff, "\n")
			my_plot.update(last_values.queue, linear_coeff, const_coeff)

			if linear_coeff_max > abs(linear_coeff):
				optimised = True
				print("Optimised!")
				time.sleep(5)
			else:
				bioreactor.node.GAS.set_flow_target(0.250)
				print("Continue!", "\n")

bioreactor.node.GAS.set_small_valves(1) # turn on N2 mode
reset(0.1)
bioreactor.node.GAS.set_small_valves(0) # turn on normal mode
