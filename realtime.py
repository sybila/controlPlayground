import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time, sys, os, math
from random import randint
import numpy as np

class Animator():
	def __init__(self, ax, xar, yar):
		self.ax = ax
		self.xar = xar
		self.yar = yar

	def init(self):
		self.ax.plot(self.xar, self.yar)

	def __call__(self, i):
		result = list(zip(*output[0]))
		#print result, SCALE
		#print "result", self.xar[-1] , result[0][0]
		if self.xar[-1] < result[0][0]:
			self.xar += result[0]
			self.yar += result[1]
			self.ax.clear()
			self.ax.plot(self.xar, self.yar)

sys.path.append(os.path.abspath('worker/'))
import SenderWorker
import ControllThread

SCALE = [1]
scales = zip(range(100, 1000, 100), range(10,100,10))
#data = list(enumerate([randint(0, 10) for p in range(0, 1000)]))
data = list(enumerate(map(lambda x: math.sin(x), range(0, 1000))))
output = [data[:100]]
firstRes = data[:100]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

firstResult = list(zip(*firstRes))
xar, yar = list(firstResult[0]), list(firstResult[1])
ud = Animator(ax, xar, yar)

controller = ControllThread.ControllThread(scales, output, SCALE)
controller.start()

sender = SenderWorker.SenderThread(data, output, SCALE)
sender.start()

ani = animation.FuncAnimation(fig, ud, frames=np.arange(500), interval=100, init_func=ud.init)
plt.show()

sender.join()
controller.join()