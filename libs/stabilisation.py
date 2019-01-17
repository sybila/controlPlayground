#import bioreactor
import numpy as np
import random
import time
import matplotlib.pyplot as plt

WAIT_TIME = 1
QUEUE_MAX_LENGTH = 10
FREQUENCY_OF_CHECK = 5

##### to simulate bioreactor #####

def simulate_pH(pH_range):
	return random.randint(pH_range[0], pH_range[1])

def simulate_set_flow(switch):
	if switch:
		return (0, 14)
	return (5, 9)

##################################

# plot results
class MyPlot():
	def __init__(self):
		plt.ion()

	def update(self, data, linear, const):
		original = np.array(data)
		x_data = np.array(range(len(original)))
		fitted = linear*x_data + const

		plt.plot(x_data, original, 'o', label='Original data', markersize=5)
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
def measure_values(last_values, pH_range, duration):
	for _ in range(duration):
		time.sleep(WAIT_TIME)
		#last_values.add(bioreactor.get_ph())
		last_values.add(simulate_pH(pH_range))
	return last_values

def reset(timeout, linear_coeff_max):
	# set_flow_target(bioreactor.MAX_FLOW) # need to define a constant for max flow
										   # can be used also for checking
	pH_range = simulate_set_flow(True)

	optimised = False
	last_values = LimitedQueue()
	my_plot = MyPlot()

	while not optimised:
		last_values = measure_values(last_values, pH_range, FREQUENCY_OF_CHECK)

		print("Check with flow ON: ", last_values.queue)
		linear_coeff, const_coeff = calculate_regression(last_values.queue)
		print("Linear coefficient: ", linear_coeff, "\n")
		my_plot.update(last_values.queue, linear_coeff, const_coeff)

		if linear_coeff_max > abs(linear_coeff):
			print("Flow turned off", "\n")
			pH_range = simulate_set_flow(False)
			last_values = measure_values(last_values, pH_range, timeout)
			print("Check with flow OFF: ", last_values.queue)
			linear_coeff, const_coeff = calculate_regression(last_values.queue)
			print("Linear coefficient: ", linear_coeff, "\n")
			my_plot.update(last_values.queue, linear_coeff, const_coeff)

			if linear_coeff_max > abs(linear_coeff):
				optimised = True
				print("Optimised!")
				time.sleep(5)
			else:
				pH_range = simulate_set_flow(True)
				print("Continue!", "\n")

#set_small_valves(1) # turn on N2 mode
reset(10, 0.1)
#set_small_valves(0) # turn on normal mode