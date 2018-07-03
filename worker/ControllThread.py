import threading
import os, time

class ControllThread(threading.Thread):
	def __init__(self, signals, output, control_signal):
		super(ControllThread, self).__init__()
		self.signals = signals
		self.output = output
		self.control_signal = control_signal
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			signal = self.findScale(self.output[0][0])
			if signal:
				self.control_signal[0] = signal

	def findScale(self, time):
		for t, s in reversed(self.signals):
			if time > t:
				return s

	def join(self, timeout=None):
		self.stoprequest.set()
		super(ControllThread, self).join(timeout)