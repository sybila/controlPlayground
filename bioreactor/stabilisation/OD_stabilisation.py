from .DataHolder import *
from .GrowthChecker import *
from .Regression import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime

OD_MAX = 0.87
OD_MIN = 0.83
TIMEOUT = 60

# turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
def pump_out_population(holder, OD_MIN, pump, TIMEOUT):
	print(holder.device.id(), "Pump out the population.")
	holder.device.set_pump_state(pump, True)
	while holder.next_value() > OD_MIN: # or make a better condition with some tolerance
		time.sleep(TIMEOUT)
	holder.device.set_pump_state(pump, False)
	print(holder.device.id(), "Minimum pupulation reached.")
	return True

# given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
# calculates current growth rate using measured OD data and exponentional regression
# has to remember initial OD!
def reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT):
	print(holder.device.id(), "Reaching max population.")
	while holder.next_value() < OD_MAX: # or make a better condition with some tolerance
		time.sleep(TIMEOUT)
	print(holder.device.id(), "Max population reached:\n",
		  "times = ", holder.times, 
		  "\n data = ", holder.data)
	return exponentional_regression(holder.times[1:], holder.data[1:], holder.data[1])

# it is called when we start with new conditions
# and they are all set for given node
# assume conditions has form [temp, co2-flow, [channel, intensity]]
def set_up_conditions(node, conditions, parameter_keys):
	funs =  {"temp": node.PBR.set_temp, 
		     "light-red": lambda intensity: node.PBR.set_light_intensity(0, intensity),
			 "light-blue": lambda intensity: node.PBR.set_light_intensity(1, intensity)}
			 # "flow": node.GAS.set_flow_target}
	success = []
	for i in range(len(parameter_keys)):
		if type(conditions[i]) == list:
			success.append(funs[parameter_keys[i]](*conditions[i]))
		else:
			success.append(funs[parameter_keys[i]](conditions[i]))
	return all(success)

def get_growth_rate(node, conditions, parameter_keys, dir_name):
	history_len = 5
	print(node.PBR.id(), "Measuring growth rate...")
	set_up_conditions(node, conditions, parameter_keys)
	print(node.PBR.id(), "Prepared given conditions.")
	checker = GrowthChecker(node.PBR.id())
	holder = DataHolder(node.PBR, time.time(), [OD_MIN, OD_MAX])
	print(node.PBR.id(), "Starting...")
	while not checker.is_stable(history_len):
		print(node.PBR.id(), "Iteration", len(checker.values))
		value = reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT)
		doubling_time = (np.log(2)/value)/3600
		print(node.PBR.id(), "New growth rate:", value, "(Doubling time:", doubling_time, "h)")
		checker.values.append(doubling_time)
		checker.times.append(time.time() - holder.init_time)
		holder.reset(value)
		pump_out_population(holder, OD_MIN, 5, TIMEOUT)
		holder.reset()
	print(node.PBR.id(), "All data measured for this conditions:\n", 
		  "times:", holder.time_history, 
		  "\n data:", holder.data_history)
	try:
		save(holder, checker, history_len, dir_name, node.PBR.id(), conditions)
	except Exception as e:
		print(node.PBR.id(), e)
	return checker.values[-1] # which should be stable

# saves data in svg and creates a picture
def save(holder, checker, history_len, dir_name, ID, conditions):
	current_time = '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now() + datetime.timedelta(hours=2))
	rows = []
	fig, ax1 = plt.subplots()

	plt.title(ID + " Stable doubling time " + "%.2f" % checker.values[-1] + " h" +\
			   "\n for conditions " + str(conditions))

	rows += list(map(lambda t, v: (t, v, None, None, None), holder.time_history, holder.data_history))
	# raw OD data
	ax1.plot(holder.time_history, holder.data_history, 'o', markersize=2)
	ax1.set_xlabel('time (s)')
	ax1.set_ylabel('OD')

	# exponencial regression of OD regions
	for data in holder.reg_history:
		times = np.linspace(data["start"], data["end"], 1000)
		values = data["n_0"] * np.exp((times-data["start"])*data["rate"])
		ax1.plot(times, values, '-b')
		rows += list(map(lambda t, v: (t, None, None, v, None), times, values))

	# checker's data
	ax2 = ax1.twinx()
	ax2.set_ylabel('doubling time (h)')
	ax2.plot(checker.times, checker.values, 'or')
	ax2.yaxis.label.set_color('red')

	rows += list(map(lambda t, v: (t, None, v, None, None), checker.times, checker.values))

	# measured growth rates
	coeffs = linear_regression(checker.times[-history_len:], checker.values[-history_len:])
	times = np.linspace(checker.times[-history_len], checker.times[-1], 500)
	values = coeffs[1] + coeffs[0]*times
	ax2.plot(times, values, '-r')

	rows += list(map(lambda t, v: (t, None, None, None, v), times, values))

	fig.tight_layout()
	plt.savefig(dir_name + "/" + ID + "/" + current_time + "_fig.svg", dpi=150)

	save_csv(rows, dir_name, ID)

def save_csv(rows, dir_name, ID):
	rows.sort(key=lambda x: x[0])
	with open(dir_name + "/" + ID + "/" + current_time + '_OD.csv', mode='w') as file:
		row_writer = csv.writer(file, delimiter=',')
		row_writer.writerow(["time", "OD", "doubling time", "expo regression", "lin regression"])
		for row in rows:
			row_writer.writerow(row)