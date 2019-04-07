import time

# it holds all measured ODs
# also is responsible for measurements and for calculation of median
# from last several measurements (due to possible errors in measurement)
class DataHolder():
	def __init__(self, device, init_time, OD_bounds):
		self.device = device
		self.init_time = init_time
		self.OD_bounds = OD_bounds
		self.data_history = []
		self.time_history = []
		self.data = []
		self.times = []
		self.outliers = []

	def measure_value(self):
		od = self.device.measure_od()
		if od is None:
			raise ValueError('Cannot measure optical density on device', self.device.ID)
		return time.time() - self.init_time, od

	def next_value(self):
		t, v = self.measure_value()
		if len(self.data) < 2:
			print("New OD value:", v)
			self.data.append(v)
			self.times.append(t)
			return v
		else:
			avg = sum(self.data[-2:])/2
			if v < (104*avg)/100 and v > (96*avg)/100: # 4% tolerance
				print("New OD value:", v)
				self.data.append(v)
				self.times.append(t)
				return v
			else:
				print("An OD outlier :", t, v)
				self.outliers.append((t,v))
				return (self.OD_bounds[0] + self.OD_bounds[1])/2 # which is always True in the conditions

	def reset(self):
		self.data_history += self.data
		self.time_history += self.times
		self.data = []
		self.times = []