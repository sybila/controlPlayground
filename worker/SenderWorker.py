import threading
import os, time
from scipy.integrate import odeint
import numpy as np

def model(x,t,control_signal):
	xdot = np.zeros(2)
	xdot[0] = control_signal*x[0]
	xdot[1] = -0.02*x[1]
	return xdot

STEP = 0.05

class SenderThread(threading.Thread):
	def __init__(self, data, output, control_signal):
		super(SenderThread, self).__init__()
		self.data = data
		self.output = output
		self.control_signal = control_signal
		self.step = STEP
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			ts = [self.step, self.step + 1]
			y = odeint(model, self.data[-1], ts, args=(self.control_signal[0],))
			self.data += y 
			self.output[0] = (self.step, y[-1])
			self.step += STEP
			time.sleep(0.2)

	def join(self, timeout=None):
		self.stoprequest.set()
		super(SenderThread, self).join(timeout)