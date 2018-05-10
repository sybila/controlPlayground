import sys
import os.path
import matplotlib.pyplot as plt
from scipy.integrate import odeint
sys.path.append(os.path.abspath('controllers/'))
sys.path.append(os.path.abspath('models/'))

# use argparse instead
modelFile = sys.argv[2]
controllerType = sys.argv[1]

if modelFile:
	exec("import " + os.path.splitext(os.path.basename(modelFile))[0] + " as model")
if controllerType == "PID":
	import PID

# constants
COLOURS = "bgcmykw"

def controlLoop():
	controller = PID.PID(model.kP, model.kI, model.kD)

	for i in range(len(model.t)-1):
		if i >= 1:  # calculate starting on second cycle
			model.u[i + 1] = controller.update(model.x0[6], model.sp[i], model.t[i+1])
		ts = [model.t[i], model.t[i+1]]

		y = odeint(model.model, model.x0, ts, args=(model.u[i + 1],))

		for j in range(7):
			model.observables[j][i+1] = y[-1][j]
			model.x0[j] = y[-1][j]

def visualise():
	# Plot the results
	plt.figure(1)
	plt.subplot(1,1,1)

	for j, variable_name in enumerate(model.plotting_vars):
		i = model.VARS.index(variable_name)
		plt.plot(model.t, model.observables[i] * model.SCALE, 'g-', color=COLOURS[j], label=variable_name)

	plt.plot(model.t, model.u * model.SCALE, 'k:', color='r', label='Control signal')
	plt.plot(model.t, model.sp * model.SCALE, 'r--', color='r', label='Set Point')
	plt.ylabel('Concentration x {0:.2e}'.format(model.SCALE))
	plt.xlabel('Time')
	plt.legend(loc='best')

	plt.show()

controlLoop()
visualise()