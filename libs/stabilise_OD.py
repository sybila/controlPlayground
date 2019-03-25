from scipy.optimize import curve_fit
import numpy as np
time

OD_MAX = 0.525
OD_MIN = 0.475
TIMEOUT = 10

# it holds all measured ODs
# also is responsible for measurements and for calculation of median
# from last several measurements (due to possible errors in measurement)
class DataHolder():
	def __init__(self, device):
		self.device = device
		self.data = []

	def measure_value(self):
		self.data.append(self.device.measure_od())

	def get_median(self, t):
		for _ in range(n):
			self.measure_value()
			time.wait(1)
		return np.median(self.data[-t:])

# once max population is computed, we obtain current growth rate and this function
# will use it and K last values to compute linear regression and decide whether
# growth is already stable (i.e. population is adapted to given conditions)
class GrowthChecker():
	def __init__(self, tolerance):
		self.values = []
		self.tolerance = tolerance

	def is_stable(self, n):
		l = len(self.values[-n:])
		times = np.linspace(1, l, l)
		coeff = linear_regression(times, self.values[-n:])
		if coeff:
			return coeff > abs(self.tolerance)
		return True

# turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
def pump_out_population(holder, OD_MIN, pump, TIMEOUT):
	holder.device.set_pump_state(pump, True)
	while holder.get_median(5) > OD_MIN: # or make a better condition with some tolerance
		time.wait(TIMEOUT)
	holder.device.set_pump_state(pump, False)
	return True

# given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
# calculates current growth rate using measured OD data and exponentional regression
# has to remember initial OD!
def reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT):
	initial = len(holder.data)
	while holder.get_median(5) < OD_MAX: # or make a better condition with some tolerance
		time.wait(TIMEOUT)
	times = np.linspace(1, len(holder.data), len(holder.data)) # could be actually measured as real time
	return exponentional_regression(times, holder.data, holder.data[initial])

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
	checker = GrowthChecker()
	holder = DataHolder(node.PBR)
	#should return True if not stabilised
	while checker.is_stable(6):
		checker.values.append(reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT))
		pump_out_population(holder, OD_MIN, pump, TIMEOUT)
	return checker.values[-1] #which should be stabile

if __name__ == '__main__':
	get_growth_rate()
