import time
import numpy as np

from bioreactor import logger

# it holds all measured ODs
# also is responsible for measurements and for calculation of median
# from last several measurements (due to possible errors in measurement)
class DataHolder(logger.Logger):
	def __init__(self, device, OD_bounds, dir_name):
		self.device = device
		self.init_time = 0
		self.OD_bounds = OD_bounds
		self.data_history = []
		self.time_history = []
		self.reg_history = []
		self.data = []
		self.times = []
		self.outliers = []

		logger.Logger.__init__(self, dir_name, self.device.ID)

	def set_init_time(self, t):
		self.init_time = t

	def measure_initial_OD(self):
		data = []
		for i in range(5):
			data.append(self.measure_value()[1])
			time.sleep(2)
		self.average = 0
		data.sort()
		print("+++++++++++++++++ OD data:", data)
		computed = False
		while not computed:
			mean = np.mean(data)
			median = np.median(data)
			if len(data) < 2:
				computed = True
				self.average = data[0]

			if mean/median <= 1:
				if mean/median >= 0.9:
					computed = True
					self.average = mean
				else:
					data = data[1:]
			else:
				data = data[:-1]

	def measure_value(self):
		od = self.device.measure_od()
		if od is None:
			self.log_error("Cannot measure OD! Trying again...")
			return self.measure_value() # try it again, should be somehow limited!
		return time.time() - self.init_time, od

	def next_value(self):
		t, v = self.measure_value()
		if v < (101.5*self.average)/100 and v > (98.5*self.average)/100: # 1.5% tolerance
			self.log("New OD value:", v)
			self.data.append(v)
			self.times.append(t)
			self.average = (self.average + v)/2 # is it OK?
			self.outliers = []
			return v
		else:
			if len(self.outliers) > 10:
				return self.reset_outliers()
			self.outliers.append((t,v))
			self.log("Outlier No." + str(len(self.outliers)) + 
					 ":", v, "with allowed range: [{0}, {1}]".format(
					(98.5*self.average)/100, (101.5*self.average)/100))
			return (self.OD_bounds[0] + self.OD_bounds[1])/2 # which is always True in the conditions

	def reset_outliers(self):
		self.log("Too many outliers, considering them as correct data.")
		self.data += [x[1] for x in self.outliers]
		self.times += [x[0] for x in self.outliers]
		self.average = sum(self.data[-2:])/2
		self.outliers = []
		return self.data[-1]

	def reset(self, value=None):
		self.data_history += self.data
		self.time_history += self.times
		if value:
			self.reg_history.append({"rate": value, "start": self.times[0],
									  "end": self.times[-1], "n_0": self.data[0]})
		self.data = []
		self.times = []