from scipy.optimize import curve_fit
import numpy as np

OD_MAX = 0.525
OD_MIN = 0.475

# turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
def pump_out_population(OD_MIN):
	pass

# given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
# calculates current growth rate using measured OD data and exponentional regression
# has to remember initial OD!
def reach_max_population(OD_MAX):
	pass

# once max population is computed, we obtain current growth rate and this function
# will use it and K last values to compute linear regression and decide whether
# growth is already stable (i.e. population is adapted to given conditions)
def growth_checker():
	pass

# measure current OD
def measure_value(device):
	return device.measure_od()

# it is called when we start with new conditions
# and they are all set for given node
def set_up_conditions(node, conditions):
	pass

# compute regression for given array of times,
# output values and initial population/density
def exponentional_regression(t, y, n_0):
	popt, pcov = curve_fit(lambda t, r: n_0 * np.exp(t * r),  t,  y)
	return popt[0]

# this should do a particle
def main():
	pass

if __name__ == '__main__':
	main()

t = np.array([1, 2, 3, 4, 5])
y = np.array([2.7, 36.9, 272.9, 2017.1, 110132.3])

# growth rate about 2, n_0 is 5
print(calculate_regression(t, y, 5))