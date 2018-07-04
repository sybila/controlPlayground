import threading

class ControllThread(threading.Thread):
	def __init__(self, set_points, output, control_signal, current_time, REFERENCE, PID):
		super(ControllThread, self).__init__()
		self.set_points = set_points
		self.output = output
		self.control_signal = control_signal
		self.current_time = current_time
		self.REFERENCE = REFERENCE
		self.PID = PID
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			#print(self.output[0][1])
			observed_value = self.output[0][1][self.REFERENCE]
			set_point = self.calculateSetPoint()
			time = self.current_time[0]
			#print(observed_value, set_point, time)
			if time > 0.5:
				signal = self.PID.update(observed_value, set_point, time)
				#print(signal)
				self.control_signal[0] = signal

	def calculateSetPoint(self):
		for t, s in reversed(self.set_points):
			if self.current_time > t:
				return s

	def join(self, timeout=None):
		self.stoprequest.set()
		super(ControllThread, self).join(timeout)