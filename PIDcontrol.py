import sys
import os.path
from scipy.integrate import odeint

sys.path.append(os.path.abspath('controllers/'))
sys.path.append(os.path.abspath('models/'))
sys.path.append(os.path.abspath('libs/'))
import progress

# constants
COLOURS = "bgcmykw"

def controlModel():
	assert len(model.plotting_vars) != 0, "There has to be at least one observable variable!"
	assert model.SCALE != 0, "Scale cannot be zero!"
	assert model.kP + model.kI + model.kD != 0, "Sum of PID parameters cannot be zero!"
	assert len(model.t) != 0, "There has to be defined time point!"
	assert len(model.t) == len(model.sp), "A set point has to be defined for every time point"

def controlLoop():
	print("Computing control...")
	controller = PID.PID(model.kP, model.kI, model.kD)
	progress_bar = progress.Progressbar(len(model.t) - 2)

	for i in range(len(model.t) - 1):
		progress_bar.printProgress(i)
		if i >= 1:  # calculate starting on second cycle
			model.u[i + 1] = controller.update(model.x0[6], model.sp[i], model.t[i+1])
		ts = [model.t[i], model.t[i+1]]

		y = odeint(model.model, model.x0, ts, args=(model.u[i + 1],))

		for j in range(7):
			model.observables[j][i+1] = y[-1][j]
			model.x0[j] = y[-1][j]

	print()

def visualiseMatplotlib():
	print("Importing visualisation library...")
	import matplotlib.pyplot as plt
	print("Visualising...")

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

def visualisePlotly():
	print("Importing visualisation library...")
	import plotly.plotly as py
	import plotly.graph_objs as go
	print("Visualising...")

	data = []
	for j, variable_name in enumerate(model.plotting_vars):
		i = model.VARS.index(variable_name)

		trace = go.Scatter(
			x = model.t,
			y = model.observables[i] * model.SCALE,
			mode = 'lines',
			name = variable_name
		)

		data.append(trace)

	trace_signal = go.Scatter(
			x = model.t,
			y = model.u * model.SCALE,
			line = dict(
				color = ('rgb(155, 0, 0)'),
				dash = 'dot'),
			name = 'Control signal'
		)
	data.append(trace_signal)

	trace_sp = go.Scatter(
			x = model.t,
			y = model.sp * model.SCALE,
			line = dict(
				color = ('rgb(255, 0, 0)'),
				dash = 'dash'),
			name = 'Set Point'
		)
	data.append(trace_sp)

	layout = dict(title = controllerType + ' control of model ' + modelName,
			  xaxis = dict(title = 'Time'),
			  yaxis = dict(title = 'Concentration x {0:.2e}'.format(model.SCALE)),
			  )

	fig = dict(data=data, layout=layout)
	py.plot(fig, filename = modelName + "_" + controllerType + "_plot")

if __name__ == '__main__':
	# use argparse instead !
	assert len(sys.argv) == 3, "Not enough arguments!"
	modelFile = sys.argv[2]
	controllerType = sys.argv[1]
	modelName = ""

	if modelFile:
		modelName = os.path.splitext(os.path.basename(modelFile))[0]
		exec("import " + modelName + " as model")
	if controllerType == "PID":
		import PID

	controlModel()
	controlLoop()
	#visualiseMatplotlib()
	visualisePlotly()