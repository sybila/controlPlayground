from .DataHolder import *
from .GrowthChecker import *
from .Regression import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime
from bioreactor import logger

class Stabiliser(logger.Logger):
	def __init__(self, node, dir_name, OD_MAX=0.87, OD_MIN=0.83, TIMEOUT=60):
		self.dir_name = dir_name
		self.node = node

		self.OD_MAX = OD_MAX
		self.OD_MIN = OD_MIN
		self.TIMEOUT = TIMEOUT

		self.checker = GrowthChecker(self.node.PBR.ID, self.dir_name)
		self.holder = DataHolder(self.node.PBR, [OD_MIN, OD_MAX], self.dir_name)

		logger.Logger.__init__(self, self.dir_name, self.node.PBR.ID)

	# turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
	def pump_out_population(self, pump):
		self.log("Reaching min population...")
		self.holder.device.set_pump_state(pump, True)
		while self.holder.next_value() > self.OD_MIN:
			time.sleep(self.TIMEOUT)
		self.holder.device.set_pump_state(pump, False)
		self.log("Min pupulation reached.")

	# given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
	# calculates current growth rate using measured OD data and exponentional regression
	# has to remember initial OD!
	def reach_max_population(self):
		self.log("Reaching max population...")
		while self.holder.next_value() < self.OD_MAX: 
			time.sleep(self.TIMEOUT)
		self.log("Max population reached:\n",
			  "times = ", self.holder.times, 
			  "\n data = ", self.holder.data)
		return exponentional_regression(self.holder.times[1:], self.holder.data[1:], self.holder.data[1])

	# it is called when we start with new conditions
	# and they are all set for given node
	# assume conditions has form [temp, co2-flow, [channel, intensity]]
	def set_up_conditions(self, conditions, parameter_keys):
		funcs =  {"temp": self.node.PBR.set_temp, 
			     "light-red": lambda intensity: self.node.PBR.set_light_intensity(0, intensity),
				 "light-blue": lambda intensity: self.node.PBR.set_light_intensity(1, intensity)}
				 # "flow": node.GAS.set_flow_target}
		success = []
		for i in range(len(parameter_keys)):
			if type(conditions[i]) == list:
				success.append(funcs[parameter_keys[i]](*conditions[i]))
			else:
				success.append(funcs[parameter_keys[i]](conditions[i]))
		return all(success)

	def get_growth_rate(self, conditions, parameter_keys, history_len=5):
		self.holder.restart()
		self.checker.restart()
		try:
			self.log("Measuring growth rate...")
			self.set_up_conditions(conditions, parameter_keys)
			self.log("Prepared given conditions.")
			self.log("Computing initial OD average...")
			self.holder.measure_initial_OD()
			self.log("Initial OD average:", self.holder.average)
			self.holder.set_init_time(time.time())
			self.log("Starting...")

			while not self.checker.is_stable(history_len):
				self.log("Iteration", len(self.checker.values))
				self.pump_out_population(5)
				self.holder.reset()
				value = self.reach_max_population()
				doubling_time = (np.log(2)/value)/3600
				self.log("New growth rate:", value, "(Doubling time:", doubling_time, "h)")
				self.checker.values.append(doubling_time)
				self.checker.times.append(time.time() - self.holder.init_time)
				self.holder.reset(value)

			self.log("All data measured for this conditions:\n", 
				  "times:", self.holder.time_history, 
				  "\n data:", self.holder.data_history)

			save(self.holder, self.checker, history_len, self.dir_name, self.node.PBR.ID, conditions)
		except Exception as e:
			self.log_error(e)
		return self.checker.values[-1] # which should be stable

# saves data in svg and creates a picture
def save(holder, checker, history_len, dir_name, ID, conditions):
	current_time = '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now() + datetime.timedelta(hours=2))
	rows = []
	fig, ax1 = plt.subplots()

	plt.title(ID + " Stable doubling time " + "%.2f" % checker.values[-1] + " h" +\
			   "\n for conditions " + str(conditions))

	rows += list(map(lambda t, v: (t, v, None, None, None), holder.time_history, holder.data_history))
	# raw OD data
	ax1.plot(to_hours(holder.time_history), holder.data_history, 'o', markersize=2)
	ax1.set_xlabel('time (h)')
	ax1.set_ylabel('OD')
	ax1.yaxis.label.set_color('blue')

	# exponencial regression of OD regions
	for data in holder.reg_history:
		times = np.linspace(data["start"], data["end"], 1000)
		values = data["n_0"] * np.exp((times-data["start"])*data["rate"])
		ax1.plot(to_hours(times), values, '-b')
		rows += list(map(lambda t, v: (t, None, None, v, None), times, values))

	# checker's data
	ax2 = ax1.twinx()
	ax2.set_ylabel('doubling time (h)')
	ax2.plot(to_hours(checker.times), checker.values, 'or')
	ax2.yaxis.label.set_color('red')

	rows += list(map(lambda t, v: (t, None, v, None, None), checker.times, checker.values))

	# measured growth rates
	coeffs = linear_regression(checker.times[-history_len:], checker.values[-history_len:])
	times = np.linspace(checker.times[-history_len], checker.times[-1], 500)
	values = coeffs[1] + coeffs[0]*times
	ax2.plot(to_hours(times), values, '-r')

	rows += list(map(lambda t, v: (t, None, None, None, v), times, values))

	fig.tight_layout()
	plt.savefig(dir_name + "/" + ID + "/" + ID + "_" + current_time + "_fig.png", dpi=150)

	save_csv(rows, dir_name, ID, current_time)

def save_csv(rows, dir_name, ID, current_time):
	rows.sort(key=lambda x: x[0])
	with open(dir_name + "/" + ID + "/" + current_time + '_OD.csv', mode='w') as file:
		row_writer = csv.writer(file, delimiter=',')
		row_writer.writerow(["time", "OD", "doubling time", "expo regression", "lin regression"])
		for row in rows:
			row_writer.writerow(row)

def to_hours(times):
	return np.array(times) / 3600