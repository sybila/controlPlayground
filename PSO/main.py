from Particle import *
from Swarm import *
import numpy as np
import bioreactor
import random

params = ["temp", "light", "flow"]

node = bioreactor.Node()
node.add_device("PBR", "PBR07", 72700007)
node.add_device("GMS", "GMS", 46700003)
node.add_device("GAS", "GAS", 42700007)

nodes = [node]

multiparametric_space = {params[0]: (20,40), params[1]: (100,800)}  # temperature and light

particles = []
swarm_results = []  # important variable shared by all particles (including swarm)

swarm = Swarm(swarm_results, multiparametric_space)

n_of_nodes = 10

for i in range(n_of_nodes):
	random_position = []
	step = random.uniform(0, 1)
	for key in swarm.parameter_keys:
		random_position.append(random.uniform(min(multiparametric_space[key]), max(multiparametric_space[key])))
	particles.append(Particle(np.array(random_position), step, swarm, nodes[0]))

swarm.start()

for particle in particles:
	particle.start()

while swarm.is_alive():
	pass # we just have to wait until the swarm particle is finished

print("************* Time to end ***********")

for particle in particles:
	# particle.join()
	particle.stoprequest.set()

print("\n++++++++++++ OVERALL RESULTS ++++++++++++\n")

for particle in particles:
	print("------- Results for particle", particle.node.PBR.ID, particle.name)
	print(particle.particle_trace)
	print()

print(swarm.swarm_best)