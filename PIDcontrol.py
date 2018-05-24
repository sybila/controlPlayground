import sys
import os.path
from scipy.integrate import odeint
import datetime

sys.path.append(os.path.abspath('controllers/'))
sys.path.append(os.path.abspath('models/'))
sys.path.append(os.path.abspath('libs/'))
import progress

controller_choices = ['PID', 'lMPC', 'nMPC']
visual_choices = ['plotly', 'matplotlib']

import argparse
parser = argparse.ArgumentParser(description='PID control of a given model.')
parser.add_argument('model', metavar='model', type=str, help='The file containing the definition of a model.')
parser.add_argument('-t', '--type', type=str,
		help='Type of the controller. Allowed values are '+', '.join(controller_choices),
		metavar='', choices=controller_choices, default='PID')
parser.add_argument('-l', '--libVis', type=str,
		help='Library for visualisation. Allowed values are '+', '.join(visual_choices),
		metavar='', choices=visual_choices, default='plotly')

# constants
COLOURS = "bgcmykw"

def checkModel():
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
			model.u[i + 1] = controller.update(model.x0[model.REFERENCE], model.sp[i], model.t[i+1])
		ts = [model.t[i], model.t[i+1]]

		y = odeint(model.model, model.x0, ts, args=(model.u[i + 1],))

		for j in range(len(model.VARS)):
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

	if model.SHOW_CONTROL_SIGNAL:
		plt.plot(model.t, model.u * model.SCALE, 'k:', color='r', label='Control signal')
	if model.SHOW_SET_POINT:
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
	if model.SHOW_CONTROL_SIGNAL:
		trace_signal = go.Scatter(
				x = model.t,
				y = model.u * model.SCALE,
				line = dict(
					color = ('rgb(155, 0, 0)'),
					dash = 'dot'),
				name = 'Control signal'
			)
		data.append(trace_signal)

	if model.SHOW_SET_POINT:
		trace_sp = go.Scatter(
				x = model.t,
				y = model.sp * model.SCALE,
				line = dict(
					color = ('rgb(255, 0, 0)'),
					dash = 'dash'),
				name = 'Set Point'
			)
		data.append(trace_sp)

	layout = dict(title = args.type + ' control of model ' + modelName + '<br>' + 
							", ".join(["kP = " + str(model.kP), 
									   "kI = " + str(model.kI),
									   "kD = " + str(model.kD)]),
			  xaxis = dict(title = 'Time'),
			  yaxis = dict(title = 'Concentration x {0:.2e}'.format(model.SCALE)),
				 )

	date = '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
	fig = dict(data=data, layout=layout)
	py.plot(fig, filename = date + " " + modelName + "_" + args.type + "_plot")

if __name__ == '__main__':
	args = parser.parse_args()

	modelName = os.path.splitext(os.path.basename(args.model))[0]
	exec("import " + modelName + " as model")
	if args.type == "PID":
		import PID

	checkModel()
	controlLoop()
	if args.libVis == 'plotly':
		visualisePlotly()
	else:
		visualiseMatplotlib()