from .Regression import *

# once max population is computed, we obtain current growth rate and this function
# will use it and K last values to compute linear regression and decide whether
# growth is already stable (i.e. population is adapted to given conditions)
class GrowthChecker():
	def __init__(self, tolerance):
		self.values = []
		self.times = []
		self.tolerance = tolerance

	def is_stable(self, n):
		coeff = abs(linear_regression(self.times, self.values[-n:]))
		avg = sum(self.values[-n:])/n
		return (coeff/avg) < self.tolerance