import threading
import numpy as np

# an Observer over all threads globally
# workers append their results to shared list
# observer takes them one by one and evaluates them
class Swarm(threading.Thread):
	def __init__(self, results, multiparametric_space):
		super(Swarm, self).__init__()

		self.type = 1 # optimum type, -1 for min
		self.swarm_results = results 
		self.boundaries = self.create_boundaries(multiparametric_space)
		self.No_of_results = 0
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			if self.swarm_results:
				new_value = self.swarm_results.pop(0)
				if new_value[1]*self.type > self.swarm_best[1]*self.type:
					self.swarm_best = new_value
				self.condition_holds()

	def condition_holds(self):
		print("Swarm:", self.No_of_results, self.swarm_best)
		self.No_of_results += 1
		if self.No_of_results > 10:
			self.stoprequest.set()

	def join(self, timeout=None):
		super(Swarm, self).join(timeout)

	def create_boundaries(self, space):
		##### JUST TOO KEEP SAME #######
		self.parameter_keys = list(space.keys())
		# self.parameter_keys = ["light-red", "light-blue"]
		################################
		self.swarm_best = []
		boundaries = [[], []]
		for key in self.parameter_keys:
			boundaries[0].append(space[key][0])
			boundaries[1].append(space[key][1])
			self.swarm_best.append(sum(boundaries[-1])/2)
		self.swarm_best = (np.array(self.swarm_best), 0)
		return boundaries

def column(i, space):
	return np.array([row[i] for row in space])