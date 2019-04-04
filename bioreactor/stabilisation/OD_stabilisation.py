from .DataHolder import *
from .GrowthChecker import *
from .Regression import *
from numpy import log

OD_MAX = 0.82
OD_MIN = 0.78
TIMEOUT = 60

# turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
def pump_out_population(holder, OD_MIN, pump, TIMEOUT):
	holder.device.set_pump_state(pump, True)
	while holder.next_value() > OD_MIN: # or make a better condition with some tolerance
		time.wait(TIMEOUT)
	holder.device.set_pump_state(pump, False)
	return True

# given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
# calculates current growth rate using measured OD data and exponentional regression
# has to remember initial OD!
def reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT):
	initial = len(holder.data)
	while holder.next_value() < OD_MAX: # or make a better condition with some tolerance
		time.wait(TIMEOUT)
	return exponentional_regression(holder.times, holder.data, holder.data[initial])

# it is called when we start with new conditions
# and they are all set for given node
# assume conditions has form [temp, co2-flow, [channel, intensity]]
def set_up_conditions(node, conditions, parameter_keys):
	functions =  {"temp": node.PBR.set_temp, 
				  "light-red": lambda intensity: node.PBR.set_light_intensity(0, intensity),
				  "light-blue": lambda intensity: node.PBR.set_light_intensity(1, intensity),
				  "flow": node.GAS.set_flow_target}
	success = []
	for i in range(len(parameter_keys)):
		if type(conditions[i]) == list:
			success.append(functions(parameter_keys[i])(*conditions[i]))
		else:
			success.append(functions(parameter_keys[i])(conditions[i]))
	return all(success)

def get_growth_rate(node, conditions, parameter_keys):
	# set initial conditions
	set_up_conditions(node, conditions, parameter_keys)
	checker = GrowthChecker(0.03)
	holder = DataHolder(node.PBR, time.time())
	#should return True if not stabilised
	while not checker.is_stable(6):
		checker.values.append(log(2)/reach_max_population(holder, OD_MIN, OD_MAX, TIMEOUT))
		checker.times.append(holder.init_time - time.time())
		pump_out_population(holder, OD_MIN, pump, TIMEOUT)
	return checker.values[-1] #which should be stable