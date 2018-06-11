import threading
import os, time

class ControllThread(threading.Thread):
	def __init__(self, scales, output, SCALE):
		super(ControllThread, self).__init__()
		self.scales = scales
		self.output = output
		self.SCALE = SCALE
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			self.SCALE[0] = self.findScale(self.output[-1][0])

	def findScale(self, value):
		for v, s in self.scales:
			if value < v:
				return s
		return self.scales[-1][1]

	def join(self, timeout=None):
		self.stoprequest.set()
		super(ControllThread, self).join(timeout)