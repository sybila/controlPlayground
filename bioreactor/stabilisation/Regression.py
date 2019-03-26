from scipy.optimize import curve_fit
import numpy as np

# compute regression for given array of times,
# output values and initial population/density
def exponentional_regression(t, y, n_0):
	popt, pcov = curve_fit(lambda t, r: n_0 * np.exp(t * r), t, y)
	return popt[0]

def linear_regression(t, y):
	popt, pcov = curve_fit(lambda t, a, b: a * t + b, times, values)
	return popt[0]