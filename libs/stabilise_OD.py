from scipy.optimize import curve_fit
import numpy as np
import time

OD_MAX = 0.525
OD_MIN = 0.475
TIMEOUT = 10

# it holds all measured ODs
# also is responsible for measurements and for calculation of median
# from last several measurements (due to possible errors in measurement)
class DataHolder():
	def __init__(self, device, init_time):
		self.device = device
		self.init_time = init_time
		self.data = []
		self.times = []

	def measure_value(self):
		return self.device.measure_od(), self.init_time - time.time()

	def next_value(self):
		t, v = self.measure_value()
		avg = sum(self.data[-2:])/2
		if v < (104*avg)/100 and v > (96*avg)/100: # 4% tolerance
			self.data.append(v)
			self.times.append(t)
			return v
		else:
			return (OD_MAX + OD_MIN)/2 # which is always True in the conditions

# once max population is computed, we obtain current growth rate and this function
# will use it and K last values to compute linear regression and decide whether
# growth is already stable (i.e. population is adapted to given conditions)
class GrowthChecker():
	def __init__(self, tolerance):
		self.values = []
		self.times = []
		self.tolerance = tolerance

	def is_stable(self, n):
		coeff = linear_regression(self.times, self.values[-n:])
		if coeff:
			return coeff > abs(self.tolerance)
		return True

# turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
def pump_out_population(holder, OD_MIN, pump, TIMEOUT):
	holder.device.set_pump_state(pump, True)
	while holder.next_value() > OD_MIN: # or make a better condition with some tolerance
		time.wait(TIMEOUT)
	holder.device.set_pump_state(pump, False)
	return True

# given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
# calculates current growth rate using measured OD data and exponentional regression
# has to remember initial OD!
def reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT):
	initial = len(holder.data)
	while holder.next_value() < OD_MAX: # or make a better condition with some tolerance
		time.wait(TIMEOUT)
	return exponentional_regression(holder.times, holder.data, holder.data[initial])

# it is called when we start with new conditions
# and they are all set for given node
# assume conditions has form [temp, co2-flow, [channel, intensity]]
def set_up_conditions(node, conditions):
	T = node.PBR.set_temp[conditions[0]]
	F = node.GAS.set_flow_target(conditions[1])
	L = node.PBR.set_light_intensity(*conditions[2])
	return (T and F and L)

# compute regression for given array of times,
# output values and initial population/density
def exponentional_regression(t, y, n_0):
	popt, pcov = curve_fit(lambda t, r: n_0 * np.exp(t * r), t, y)
	return popt[0]

def linear_regression(t, y):
	popt, pcov = curve_fit(lambda t, a, b: a * t + b, times, values)
	return popt[0]

# this is a function called by a particle, provides growth rate for given conditions
def get_growth_rate(node, conditions):
	# set initial conditions
	set_up_conditions(node, conditions)
	checker = GrowthChecker(0.01)
	holder = DataHolder(node.PBR, time.time())
	#should return True if not stabilised
	while checker.is_stable(6):
		checker.values.append(reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT))
		checker.times.append(holder.init_time - time.time())
		pump_out_population(holder, OD_MIN, pump, TIMEOUT)
	return checker.values[-1] #which should be stable

if __name__ == '__main__':
	get_growth_rate()
