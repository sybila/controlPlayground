import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time, sys, os, math
from random import randint
import numpy as np

class Animator():
	def __init__(self, ax, xar, yarA, yarB):
		self.ax = ax
		self.xar = xar
		self.yarA = yarA
		self.yarB = yarB

	def init(self):
		self.ax.plot(self.xar, self.yarA)
		self.ax.plot(self.xar, self.yarB)

	def __call__(self, i):
		if self.xar[-1] < output[0][0]:
			self.xar += [output[0][0]]
			self.yarA += [output[0][1][0]]
			self.yarB += [output[0][1][1]]
			self.ax.clear()
			self.ax.plot(self.xar, self.yarA)
			self.ax.plot(self.xar, self.yarB)

sys.path.append(os.path.abspath('worker/'))
import SenderWorker
import ControllThread

SCALE = [1]
scales = zip(range(100, 1000, 100), range(10,100,10))
#data = list(enumerate([randint(0, 10) for p in range(0, 1000)]))
data = [[10, 1]]
output = [(0, 0)]
firstRes = [(0, 0, 0)]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

firstResult = list(zip(*firstRes))
xar, yarA, yarB = list(firstResult[0]), list(firstResult[1]), list(firstResult[2])
ud = Animator(ax, xar, yarA, yarB)

controller = ControllThread.ControllThread(scales, output, SCALE)
controller.start()

sender = SenderWorker.SenderThread(data, output, SCALE)
sender.start()

ani = animation.FuncAnimation(fig, ud, frames=np.arange(500), interval=100, init_func=ud.init)
plt.show()

sender.join()
controller.join()