from .DataHolder import *
from .GrowthChecker import *
from .Regression import *
from numpy import log
import datetime

OD_MAX = 0.82
OD_MIN = 0.78
TIMEOUT = 60

# turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
def pump_out_population(holder, OD_MIN, pump, TIMEOUT):
	print(datetime.datetime.now()+datetime.timedelta(hours=2), "| Pump out the population.")
	holder.device.set_pump_state(pump, True)
	while holder.next_value() > OD_MIN: # or make a better condition with some tolerance
		time.sleep(TIMEOUT)
	holder.device.set_pump_state(pump, False)
	print("Minimum pupulation reached.")
	return True

# given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
# calculates current growth rate using measured OD data and exponentional regression
# has to remember initial OD!
def reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT):
	print(datetime.datetime.now()+datetime.timedelta(hours=2), "| Reaching max population.")
	while holder.next_value() < OD_MAX: # or make a better condition with some tolerance
		time.sleep(TIMEOUT)
	print("Max population reached:")
	print("times = ", holder.times, "\n data = ", holder.data)
	return exponentional_regression(holder.times - holder.times[0], holder.data, holder.data[0])

# it is called when we start with new conditions
# and they are all set for given node
# assume conditions has form [temp, co2-flow, [channel, intensity]]
def set_up_conditions(node, conditions, parameter_keys):
	funs =  {"temp": node.PBR.set_temp, 
				  "light-red": lambda intensity: node.PBR.set_light_intensity(0, intensity),
				  "light-blue": lambda intensity: node.PBR.set_light_intensity(1, intensity),
				  "flow": node.GAS.set_flow_target}
	success = []
	for i in range(len(parameter_keys)):
		if type(conditions[i]) == list:
			success.append(funs[parameter_keys[i]](*conditions[i]))
		else:
			success.append(funs[parameter_keys[i]](conditions[i]))
	return all(success)

def get_growth_rate(node, conditions, parameter_keys):
	history_len = 6
	print("------------------------")
	print(datetime.datetime.now()+datetime.timedelta(hours=2), "| Measuring growth rate....")
	set_up_conditions(node, conditions, parameter_keys)
	print(datetime.datetime.now()+datetime.timedelta(hours=2), "| Prepared given conditions...")
	checker = GrowthChecker(0.03)
	holder = DataHolder(node.PBR, time.time(), [OD_MIN, OD_MAX])
	print("Starting...")
	while not checker.is_stable(history_len):
		print(datetime.datetime.now()+datetime.timedelta(hours=2), "| Iteration", len(checker.values))
		value = reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT)
		print(datetime.datetime.now()+datetime.timedelta(hours=2), "| New growth rate:", value, " - Doubling time:", log(2)/value)
		checker.values.append(log(2)/value)
		checker.times.append(time.time() - holder.init_time)
		holder.reset()
		pump_out_population(holder, OD_MIN, 5, TIMEOUT)
		holder.reset()
	print("All data measured for this conditions:")
	print("Times:", holder.time_history)
	print("Data:", holder.data_history)
	return checker.values[-1] # which should be stable