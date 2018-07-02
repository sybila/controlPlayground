import threading
import os, time
from scipy.integrate import odeint
import numpy as np

def model(x,t,control_signal):
	xdot = np.zeros(2)
	xdot[0] = 0.05*x[0]
	xdot[1] = -0.02*x[0]
	return xdot

STEP = 1

class SenderThread(threading.Thread):
	def __init__(self, data, output, SCALE):
		super(SenderThread, self).__init__()
		self.data = data
		self.output = output
		self.SCALE = SCALE
		self.step = STEP
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			ts = [self.step, self.step + 1]
			y = odeint(model, self.data[-1], ts, args=(5,))
			print(y)
			self.data += y 
			self.output[0] = (self.step, y[-1])
			self.step += STEP
			time.sleep(1)

	def join(self, timeout=None):
		self.stoprequest.set()
		super(SenderThread, self).join(timeout)