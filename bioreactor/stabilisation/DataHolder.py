import time

# it holds all measured ODs
# also is responsible for measurements and for calculation of median
# from last several measurements (due to possible errors in measurement)
class DataHolder():
	def __init__(self, device, init_time):
		self.device = device
		self.init_time = init_time
		self.data = []
		self.times = []

	def measure_value(self):
		return self.device.measure_od(), self.init_time - time.time()

	def next_value(self):
		t, v = self.measure_value()
		avg = sum(self.data[-2:])/2
		if v < (104*avg)/100 and v > (96*avg)/100: # 4% tolerance
			self.data.append(v)
			self.times.append(t)
			return v
		else:
			return (OD_MAX + OD_MIN)/2 # which is always True in the conditions