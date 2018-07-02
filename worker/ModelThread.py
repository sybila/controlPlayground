import threading
import os, time
import sys
import os.path

sys.path.append(os.path.abspath('../models/'))

STEP = 100

class SenderThread(threading.Thread):
	def __init__(self, control_signal, t, current_time, model, output):
		super(SenderThread, self).__init__()
		self.current_time = current_time
		self.t = t
		self.control_signal = control_signal
		self.model = model
		self.output = output
		self.stoprequest = threading.Event()

	def run(self):
		print("Computing control...")
		while not self.stoprequest.isSet():
			for i in range(len(self.t) - 1):
				self.current_time[0] = self.t[i]
				ts = [self.t[i], self.t[i+1]]
				self.output[0] = self.model.calculateNextStep(ts, self.control_signal)
				time.sleep(self.t[i+1] - self.t[i])
			self.stoprequest.set()
			print("Finished...")

	def join(self, timeout=None):
		self.stoprequest.set()
		super(SenderThread, self).join(timeout)