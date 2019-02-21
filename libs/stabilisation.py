import bioreactor
import numpy as np
import random
import time
import matplotlib.pyplot as plt

WAIT_TIME = 5  #... chceme merat kazdych 30 sekund
QUEUE_MAX_LENGTH = 10  # poslednych 20 merani
TIMEOUT = 30 # in seconds
LINEAR_COEFF = 0.1

##################################

# plot results
class MyPlot():
	def __init__(self, queue_length):
		plt.ion()
		self.x = np.array([])
		self.y = np.array([])
		self.queue_length = queue_length

	def get_last_x(self):
		if len(self.x) == 0:
			return 0
		return int(self.x[-1])

	def get_last_n(self):
		return self.y[-self.queue_length:]

	def update_data(self, new_y):
		self.y = np.append(self.y, new_y)
		if len(self.x) > self.queue_length:
			self.x = np.append(self.x - 1, self.queue_length)
		else:
			self.x = np.append(self.x, self.get_last_x() + 1)

		plt.plot(self.x, self.y, 'o', label='Original data', markersize=5)
		plt.draw()
		plt.pause(0.0001)
		plt.clf()

	def update_fit(self, linear, const):
		x_data = self.x[-self.queue_length:]
		fitted = linear*x_data + const
		plt.plot(self.x, self.y, 'o', label='Original data', markersize=5)
		plt.plot(x_data, fitted, 'r', label='Fitted line')
		plt.draw()
		plt.pause(0.0001)
		plt.clf()

# computes regression
def calculate_regression(data):
	x = np.array(range(len(data)))
	y = np.array(data)
	A = np.vstack([x, np.ones(len(x))]).T
	linear_coeff, const_coeff = np.linalg.lstsq(A, y, rcond=None)[0]
	return linear_coeff, const_coeff

def measure_value(plot):
	plot.update_data(bioreactor.node.PBR.get_ph())

def reset(linear_coeff_max, queue_length, wait_time, timeout):
	bioreactor.node.GAS.set_flow_target(0.250)

	my_plot = MyPlot(queue_length)

	for _ in range(queue_length):
		time.sleep(wait_time)
		measure_value(my_plot)

	optimised = False

	while not optimised:
		linear_coeff, const_coeff = calculate_regression(my_plot.get_last_n())
		my_plot.update_fit(linear_coeff, const_coeff)

		print("Check with flow ON: ", my_plot.get_last_n())
		print("Linear coefficient: ", linear_coeff, "\n")

		if linear_coeff_max > abs(linear_coeff):
			print("Flow turned off", "\n")
			bioreactor.node.GAS.set_flow_target(0)
			for _ in range(timeout//wait_time):
				time.sleep(wait_time)
				measure_value(my_plot)
			print("Check with flow OFF: ", my_plot.get_last_n())
			linear_coeff, const_coeff = calculate_regression(my_plot.get_last_n())
			print("Linear coefficient: ", linear_coeff, "\n")
			my_plot.update_fit(linear_coeff, const_coeff)

			if linear_coeff_max > abs(linear_coeff):
				optimised = True
				print("Optimised!")
				time.sleep(5)
			else:
				bioreactor.node.GAS.set_flow_target(0.250)
				print("Continue!", "\n")
		time.sleep(wait_time)

bioreactor.node.GAS.set_small_valves(1) # turn on N2 mode
reset(LINEAR_COEFF, QUEUE_MAX_LENGTH, WAIT_TIME, TIMEOUT)
bioreactor.node.GAS.set_small_valves(0) # turn on normal mode
