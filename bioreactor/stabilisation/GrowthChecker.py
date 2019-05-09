from scipy.stats import sem, t
from scipy import mean

from .Regression import *
from bioreactor import logger

# once max population is computed, we obtain current growth rate and this function
# will use it and K last values to compute linear regression and decide whether
# growth is already stable (i.e. population is adapted to given conditions)
class GrowthChecker(logger.Logger):
	def __init__(self, device_id, dir_name, linear_tol, confidence_tol):
		self.values = []
		self.times = []
		self.device_id = device_id
		self.linear_tol = linear_tol
		self.confidence_tol = confidence_tol

		logger.Logger.__init__(self, dir_name, device_id)

	def is_stable(self, n):
		self.log("Checking for stability with:\n",
			  "times = ", self.times[-n:], 
			  "data = ", self.values[-n:])
		if len(self.values) < n:
			self.log("Not enough values to check")
			return False
		avg = mean(self.values[-n:])
		return self.regression_criteria(avg, n) and self.confidence_criteria(avg, n)

	def regression_criteria(self, avg, n):
		coeff = abs(linear_regression(self.times[-n:], self.values[-n:])[0])
		self.log("Regression check:", (coeff/avg), "<", self.linear_tol, "? :", (coeff/avg) < self.linear_tol)
		return (coeff/avg) < self.linear_tol

	def confidence_criteria(self, avg, n, confidence=0.95):
		std_err = sem(self.values[-n:])
		h = std_err * t.ppf((1 + confidence) / 2, n - 1)
		self.log("Confidence check:", (h/avg), "<", self.confidence_tol, "? :", (h/avg) < self.confidence_tol)
		return (h/avg) < self.confidence_tol

	def restart(self):
		self.values = []
		self.times = []