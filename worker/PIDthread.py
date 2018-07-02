import threading
import os, time

class ControllThread(threading.Thread):
	def __init__(self, control_signal, signals, current_time, output):
		super(ControllThread, self).__init__()
		self.control_signal = control_signal
		self.signals = signals
		self.current_time = current_time
		self.output = output
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			self.control_signal[0] = self.computeSignal()

	def computeSignal(self):
		for v, s in self.signals:
			if self.current_time < v:
				return s
		return self.signals[-1][1]

	def join(self, timeout=None):
		self.stoprequest.set()
		super(ControllThread, self).join(timeout)