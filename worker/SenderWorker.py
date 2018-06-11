import threading
import os, time

STEP = 10

class SenderThread(threading.Thread):
	def __init__(self, data, output):
		super(SenderThread, self).__init__()
		self.data = data
		self.output = output
		self.step = STEP
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			self.output += self.data[self.step:self.step + STEP]
			self.step += STEP
			time.sleep(0.1)

	def join(self, timeout=None):
		self.stoprequest.set()
		super(SenderThread, self).join(timeout)