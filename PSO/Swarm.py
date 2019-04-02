import threading
import numpy as np

# an Observer over all threads globally
# workers append their results to shared list
# observer takes them one by one and evaluates them
class Swarm(threading.Thread):
	def __init__(self, results, multiparametric_space):
		super(Swarm, self).__init__()
		self.swarm_results = results
		self.swarm_best = (find_center(multiparametric_space), 0)

		self.multiparametric_space = create_boundaries(multiparametric_space)
		self.No_of_results = 0
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			if self.swarm_results:
				new_value = self.swarm_results.pop()
				if new_value[1] > self.swarm_best[1]:
					self.swarm_best = new_value
				self.condition_holds()

	def condition_holds(self):
		print("Swarm:", self.No_of_results, self.swarm_best)
		self.No_of_results += 1
		if self.No_of_results > 100:
			self.stoprequest.set()

	def join(self, timeout=None):
		super(Swarm, self).join(timeout)


def find_center(space):
	return np.array(list(map(lambda v: sum(v)/2, space)))

def create_boundaries(space):
	return [column(0, space), column(1, space)]

def column(i, space):
	return np.array([row[i] for row in space])