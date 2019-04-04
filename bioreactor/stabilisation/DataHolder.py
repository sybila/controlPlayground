import time

# it holds all measured ODs
# also is responsible for measurements and for calculation of median
# from last several measurements (due to possible errors in measurement)
class DataHolder():
	def __init__(self, device, init_time, OD_bounds):
		self.device = device
		self.init_time = init_time
		self.OD_bounds = OD_bounds
		self.data = []
		self.times = []

	def measure_value(self):
		print("Measuring OD...")
		od = self.device.measure_od()
		if od is None:
			raise ValueError('Cannot measure optical density on device', self.device.ID)
		return time.time() - self.init_time, od

	def next_value(self):
		t, v = self.measure_value()
		avg = sum(self.data[-2:])/2
		if v < (104*avg)/100 and v > (96*avg)/100: # 4% tolerance
			print("New OD data:", v)
			self.data.append(v)
			self.times.append(t)
			return v
		else:
			return (self.OD_bounds[0] + self.OD_bounds[1])/2 # which is always True in the conditions

	def measure_initial(self, n, timeout):
		for i in range(n):
			print("Initial measure", i)
			self.data.append(self.device.measure_od())
			self.times.append(time.time() - self.init_time)
			time.sleep(timeout/2)
