import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time, sys, os, math
from random import randint

sys.path.append(os.path.abspath('worker/'))
import SenderWorker
import ControllThread

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
	result = list(zip(*output))
	xar, yar = result[0], [x * SCALE[0] for x in result[1]]
	ax1.clear()
	ax1.plot(xar,yar)

SCALE = [1]
scales = zip(range(100, 1000, 100), range(10,100,10))
#data = list(enumerate([randint(0, 9) for p in range(0, 1000)]))
data = list(enumerate(map(lambda x: math.sin(x), range(0, 1000))))
output = data[:10]

controller = ControllThread.ControllThread(scales, output, SCALE)
controller.start()

sender = SenderWorker.SenderThread(data, output)
sender.start()

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()

sender.join()
controller.join()