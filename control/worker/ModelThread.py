import threading
import os, time
import sys
import os.path

sys.path.append(os.path.abspath('../models/'))

STEP = 0.01

class SenderThread(threading.Thread):
	def __init__(self, control_signal, current_time, model, output):
		super(SenderThread, self).__init__()
		self.current_time = current_time
		self.control_signal = control_signal
		self.model = model
		self.output = output
		self.step = STEP
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			ts = [self.step, self.step + STEP]
			self.current_time[0] = self.step
			self.output[0] = (self.step, self.model.calculateNextStep(ts, self.control_signal[0]))
			self.step += STEP
			time.sleep(0.1)

	def join(self, timeout=None):
		self.stoprequest.set()
		super(SenderThread, self).join(timeout)