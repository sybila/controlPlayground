from .Regression import *
from scipy.stats import sem, t
from scipy import mean

# once max population is computed, we obtain current growth rate and this function
# will use it and K last values to compute linear regression and decide whether
# growth is already stable (i.e. population is adapted to given conditions)
class GrowthChecker():
	def __init__(self, linear_tol=0.04, confidence_tol=0.06):
		self.values = []
		self.times = []
		self.linear_tol = linear_tol
		self.confidence_tol = confidence_tol

	def is_stable(self, n):
		print("Checking for stability with:\n",
			  "times = ", self.times[-n:], 
			  "data = ", self.values[-n:])
		if len(self.values) < n:
			print("Not enough values to check")
			return False
		avg = mean(self.values[-n:])
		return self.regression_criteria(avg) and self.confidence_criteria(avg, n)

	def regression_criteria(self, avg):
		coeff = abs(linear_regression(self.times[-n:], self.values[-n:])[0])
		print("Regression check:", (coeff/avg), "<", self.linear_tol, "? :", (coeff/avg) < self.tolerance)
		return (coeff/avg) < self.linear_tol

	def confidence_criteria(self, avg, n, confidence=0.95):
		std_err = sem(self.values[-n:])
		h = std_err * t.ppf((1 + confidence) / 2, n - 1)
		print("Confidence check:",(h/avg), "<", self.confidence_tol, "? :", (h/avg) < self.confidence_tol)
		return (h/avg) < self.confidence_tol