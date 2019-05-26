from scipy.optimize import curve_fit
import numpy as np


# compute regression for given array of times,
# output values and initial population/density
def exponentional_regression(times, values, n_0, initial_param=0.0001):
    times = np.array(times) - times[0]
    popt, pcov = curve_fit(lambda t, r: n_0 * np.exp(t * r), times, np.array(values), maxfev=2000, p0=initial_param)
    # print("Exponentional regression:", popt, pcov)
    return popt[0]


def linear_regression(times, values):
    popt, pcov = curve_fit(lambda t, a, b: a * t + b, times, values)
    return popt
