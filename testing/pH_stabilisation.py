import bioreactor
import logger
import numpy as np
import random
import time
import matplotlib.pyplot as plt

# all in seconds
WAIT_TIME = 20  # how often we want to check the pH
QUEUE_MAX_LENGTH = 20  # how many measures consider in linear regression
TIMEOUT = 300 # after stabilisation, how long to wait to be sure it is really stable

LINEAR_COEFF = 0.01 # max allows linear coefficient of linear regression
silent_mode = False # True to disable graphical output

##################################

# plot results
class Progress():
	def __init__(self, queue_length, silent_mode, wait_time):
		plt.ion()
		plt.xlabel('time [s]')
		plt.ylabel('pH')
		self.time = np.array([])
		self.data = np.array([])
		self.queue_length = queue_length
		self.silent_mode = silent_mode
		self.wait_time = wait_time

	def get_last_time(self):
		if len(self.time) == 0:
			return 0
		return self.time[-1]

	def get_last_n_data(self):
		return self.data[-self.queue_length:]

	def get_last_n_time(self):
		return self.time[-self.queue_length:]

	def update_data(self, new_y):
		print("(", time.strftime("%H:%M:%S"), ") New value: ", new_y, "\n")
		self.data = np.append(self.data, new_y)
		self.time = np.append(self.time, self.get_last_time() + 1)

		if not self.silent_mode:
			plt.plot(self.time*self.wait_time, self.data, 'o', label='Original data', markersize=5)
			plt.draw()
			plt.pause(0.0001)
			plt.clf()

	def update_fit(self, linear, const):
		fitted = linear*self.get_last_n_time() + const
		plt.plot(self.time*self.wait_time, self.data, 'o', label='Original data', markersize=5)
		plt.plot(self.get_last_n_time()*self.wait_time, fitted, 'r', label='Fitted line')
		plt.draw()
		plt.pause(0.0001)
		plt.clf()

	def save(self):
		name = time.strftime("%Y%m%d-%H%M%S")
		fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
		ax.plot(self.time*self.wait_time, self.data, 'o', label='Original data', markersize=5)
		fig.savefig('.log/' + name + '.png')
		plt.close(fig)

# computes regression
def calculate_regression(plot):
	x = plot.get_last_n_time()
	y = plot.get_last_n_data()
	A = np.vstack([x, np.ones(len(x))]).T
	linear_coeff, const_coeff = np.linalg.lstsq(A, y, rcond=None)[0]
	return linear_coeff, const_coeff

def measure_value(progress):
	progress.update_data(bioreactor.node.PBR.get_ph())

def reset(linear_coeff_max, queue_length, wait_time, timeout, silent_mode):
	bioreactor.node.GAS.set_flow_target(0.250)

	progress = Progress(queue_length, silent_mode, wait_time)

	for _ in range(queue_length):
		time.sleep(wait_time)
		measure_value(progress)

	optimised = False

	while not optimised:
		linear_coeff, const_coeff = calculate_regression(progress)
		if not silent_mode:
			progress.update_fit(linear_coeff, const_coeff)

		print("Check with flow ON: \nData: ", progress.get_last_n_data())
		print("Linear coefficient: ", linear_coeff, "(goal is: <", linear_coeff_max, ")\n")

		if linear_coeff_max > abs(linear_coeff):
			print("Flow turned off", "\n")
			bioreactor.node.GAS.set_flow_target(0)
			for _ in range(timeout//wait_time):
				time.sleep(wait_time)
				measure_value(progress)
			print("Check with flow OFF: \nData: ", progress.get_last_n_data())
			linear_coeff, const_coeff = calculate_regression(progress)
			print("Linear coefficient: ", linear_coeff, "(goal is: <", linear_coeff_max, ")\n")
			if not silent_mode:
				progress.update_fit(linear_coeff, const_coeff)

			if linear_coeff_max > abs(linear_coeff):
				optimised = True
				print("Value stabilised!")
				progress.save()
				time.sleep(5)
			else:
				bioreactor.node.GAS.set_flow_target(0.250)
				print("Not stabilised, continue!", "\n")
		time.sleep(wait_time)
		measure_value(progress)

bioreactor.node.GAS.set_small_valves(1) # turn on N2 mode
reset(LINEAR_COEFF, QUEUE_MAX_LENGTH, WAIT_TIME, TIMEOUT, silent_mode)
bioreactor.node.GAS.set_small_valves(0) # turn on Co2 mode
bioreactor.node.GAS.set_flow_target(0.005)
