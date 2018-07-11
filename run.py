import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time, sys, os, math
from random import randint
import numpy as np

sys.path.append(os.path.abspath('controllers/'))
import PID

def convergence(signal):
	return (0.03*signal)/1e+6

class Animator():
    def __init__(self, ax, xar, yar, model):
        self.ax = ax
        self.xar = xar
        self.yar = yar
        self.signal = [convergence(control_signal[0])]
        self.goal = [set_point[0]]
        self.model = model

    def __call__(self, i):
        if self.xar[-1] < output[0][0]:
            self.xar += [output[0][0]]
            self.yar += [output[0][1][REFERENCE]]
            self.signal += [convergence(control_signal[0])]
            self.goal += set_point
            self.ax.clear()
            self.ax.plot(self.xar, self.yar, label='Variable')
            self.ax.plot(self.xar, self.signal, label='Signal')
            self.ax.plot(self.xar, self.goal, label='Set Point')

            self.ax.legend()


sys.path.append(os.path.abspath('worker/'))
import ModelThread
import PIDthread
sys.path.append(os.path.abspath('models/'))
from muller import *
import Model

control_signal = [5000]
set_point = [0.00015]
current_time = [0]
output = [(0, [0]*7)]
model = Model.Model(x0, VARS, plotting_vars, SCALE, control_signal, REFERENCE, ODEs, parameters)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

xar, yar = [0], [0]
ud = Animator(ax, xar, yar, model)

pid = PID.PID(kP, kI, kD)
controller = PIDthread.ControllThread(set_points, output, control_signal, current_time, REFERENCE, pid, set_point)
controller.start()

sender = ModelThread.SenderThread(control_signal, current_time, model, output)
sender.start()

ani = animation.FuncAnimation(fig, ud, frames=np.arange(500), interval=100)
plt.show()

sender.join()
controller.join()