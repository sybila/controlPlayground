import threading
import os, time

STEP = 100

class SenderThread(threading.Thread):
	def __init__(self, data, output, SCALE):
		super(SenderThread, self).__init__()
		self.data = data
		self.output = output
		self.SCALE = SCALE
		self.step = STEP
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet() and self.step < len(self.data):
			temp_data = self.data[self.step:self.step + STEP]
			temp_data = map(lambda d: (d[0], d[1]*self.SCALE[0]), temp_data)
			self.output[0] = temp_data
			self.step += STEP
			time.sleep(1)

	def join(self, timeout=None):
		self.stoprequest.set()
		super(SenderThread, self).join(timeout)