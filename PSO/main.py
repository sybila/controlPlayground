from Particle import *
from Swarm import *
import numpy as np
import bioreactor
import random

params = ["temp", "light-red", "light-blue", "flow"]

node = bioreactor.Node()
node.add_device("PBR", "PBR07", 72700007)
node.add_device("GMS", "GMS", 46700003)
node.add_device("GAS", "GAS", 42700007)

############ initial setup #############
node.PBR.set_temp(25)
node.GMS.set_valve_flow(0, 0.01)
node.GMS.set_valve_flow(1, 0.33)
node.GAS.get_flow_target(0.2)
node.PBR.set_pwm(50, True)
########################################

nodes = [node]

multiparametric_space = {params[1]: (50, 400), # red light
						 params[2]: (50, 400)} # blue light

particles = []
swarm_results = []  # important variable shared by all particles (including swarm)

swarm = Swarm(swarm_results, multiparametric_space)

n_of_nodes = 1

for i in range(n_of_nodes):
	random_position = []
	step = random.uniform(0, 1)
	for key in swarm.parameter_keys:
		random_position.append(random.uniform(min(multiparametric_space[key]), max(multiparametric_space[key])))
	particles.append(Particle(np.array(random_position), step, swarm, nodes[i]))

swarm.start()

for particle in particles:
	particle.start()

while swarm.is_alive():
	pass # we just have to wait until the swarm particle is finished

print("************* Time to end ***********")

for particle in particles:
	particle.stoprequest.set()

print("\n++++++++++++ OVERALL RESULTS ++++++++++++\n")

values = []
for particle in particles:
	print("------- Results for particle", particle.node.PBR.ID, particle.name)
	print(particle.particle_trace)
	values.append(max(column(1, particle.particle_trace)))
	print("BEST:", values[-1])

print("ACtual best:", max(values))
print('Swarm best:', swarm.swarm_best)