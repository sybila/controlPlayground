import threading
import numpy as np
import csv

import matplotlib
matplotlib.use('Agg')
matplotlib.rc('figure', max_open_warning = 0)
import matplotlib.pyplot as plt

import bioreactor

COLOURS = "bgrcmyk"

# an Observer over all threads globally
# workers append their results to shared list
# observer takes them one by one and evaluates them
class Swarm(threading.Thread):
	def __init__(self, multiparametric_space, dir_name, optimum_type=-1):
		super(Swarm, self).__init__()

		self.optimum_type = optimum_type # optimum type, -1 for min
		self.swarm_results = [] 
		self.boundaries = self.create_boundaries(multiparametric_space)
		self.No_of_results = 0
		self.stoprequest = threading.Event()
		self.log = open(dir_name + "/history.log", "a")
		self.dir_name = dir_name
		self.particles = []

	def run(self):
		while not self.stoprequest.isSet():
			if self.swarm_results:
				new_value = self.swarm_results.pop(0)
				if new_value[1]*self.optimum_type > self.swarm_best[1]*self.optimum_type:
					self.swarm_best = new_value
				self.condition_holds()
		self.exit()

	def condition_holds(self):
		self.log.write(bioreactor.show_time() + "Swarm best so far: No " +
					str(self.No_of_results) + ", best: " + str(self.swarm_best) + "\n")
		self.log.flush()
		self.No_of_results += 1
		if self.No_of_results > 100:
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
		self.swarm_best = (np.array(self.swarm_best), - self.optimum_type * np.inf)
		return boundaries

	def add_particle(self, particle):
		if particle.node.PBR.ID in map(lambda p: p.node.PBR.ID, self.particles):
			print("Device already exists.")
		else:
			particle.start()
			self.particles.append(particle)

	def remove_particle(self, ID):
		particle = self.particles.pop(ID)
		particle.exit()

	def exit(self):
		for particle in self.particles:
			particle.exit()
		self.stoprequest.set()

	def save(self):
		self.rows = []
		self.header = list(self.parameter_keys)
		n_params = len(self.parameter_keys)
		n_particles = len(self.particles)
		for i, particle in enumerate(self.particles):
			self.header.append(particle.node.PBR.ID)
			for point in particle.particle_trace:
				row = [None] * (n_particles + n_params)
				row[0:n_params] = point[0]
				row[i+n_params] = point[1]
				self.rows.append(row)
		self.save_csv()
		self.save_plot()

	def save_csv(self):
		with open(self.dir_name + '/results.csv', mode='w') as file:
			row_writer = csv.writer(file, delimiter=',')
			row_writer.writerow(self.header)
			for row in self.rows:
				row_writer.writerow(row)

	def save_plot(self):
		f, ax = plt.subplots()

		for i, particle in enumerate(self.particles):
			temps = temp(particle.particle_trace)
			ODs = OD(particle.particle_trace)
			ax.plot(temps, ODs, '-' + COLOURS[i], label=particle.node.PBR.ID)
			ax.plot(temps[0], ODs[0], '>' + COLOURS[i], label=particle.node.PBR.ID + ' start')
			ax.plot(temps[-1], ODs[-1], '*'  + COLOURS[i], label=particle.node.PBR.ID + ' end')

		ymin, ymax = ax.get_ylim()
		ax.set_yticks(np.round(np.linspace(ymin, ymax, 10), 2))

		xmin, xmax = ax.get_xlim()
		ax.set_xticks(np.round(np.linspace(xmin, xmax, 10), 2))

		legend = ax.legend(shadow=True)

		plt.savefig(self.dir_name + "/results.png", dpi=150)

def temp(data):
	return [d[0][0] for d in data]

def OD(data):
	return [d[1] for d in data]