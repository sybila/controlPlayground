import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time, sys, os, math
from random import randint
import numpy as np

class Animator():
    def __init__(self, ax, xar, yar, model):
        self.ax = ax
        self.xar = xar
        self.yar = yar
        self.model = model

    def __call__(self, i):
        print("here", output)
        #print result, SCALE
        #print "result", self.xar[-1] , result[0][0]
        if self.xar[-1] < output[0][0]:
            self.xar += output[0]
            self.yar += output[1]
            #self.ax.clear()
            #self.ax.plot(self.xar, self.yar)

sys.path.append(os.path.abspath('worker/'))
import ModelThread
import PIDthread
sys.path.append(os.path.abspath('models/'))
from muller import *
import Model

control_signal = [controls[0][1]]
current_time = [0]
output = [[0]]
model = Model.Model(x0, VARS, plotting_vars, SCALE, control_signal, observables, REFERENCE, ODEs)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

xar, yar = [0], [0]
ud = Animator(ax, xar, yar, model)

controller = PIDthread.ControllThread(control_signal, controls, current_time, output)
controller.start()

sender = ModelThread.SenderThread(control_signal, t, current_time, model, output)
sender.start()

ani = animation.FuncAnimation(fig, ud, frames=np.arange(500), interval=100)
plt.show()

sender.join()
controller.join()