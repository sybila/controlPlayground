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
			signal = self.computeSignal()
			if signal:
				self.control_signal[0] = signal

	def computeSignal(self):
		for t, s in reversed(self.signals):
			if self.current_time[0] > t:
				return s

	def join(self, timeout=None):
		self.stoprequest.set()
		super(ControllThread, self).join(timeout)