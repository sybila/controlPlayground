import numpy as np
import random
import os, sys
import datetime
import time

from Particle import *
from Swarm import *
import bioreactor

now =  datetime.datetime.now() + datetime.timedelta(hours=2)
dir_name = ".log/" + '{:%Y%m%d-%H%M%S}'.format(now)
os.mkdir(dir_name)

node_IDs = ["PBR02", "PBR03", "PBR07"]

for ID in node_IDs:
	os.mkdir(dir_name + "/" + ID)

params = ["temp", "light-red", "light-blue", "flow"]

print("Initial setup...")

#node1 = bioreactor.Node(1)
#node1.add_device("PBR", "PBR01", 72700001)
# node.add_device("GMS", "GMS", 46700003)
# node.add_device("GAS", "GAS", 42700007)

node2 = bioreactor.Node(2)
node2.add_device("PBR", "PBR02", 72700002)
node2.setup_stabiliser(dir_name)

node3 = bioreactor.Node(3)
node3.add_device("PBR", "PBR03", 72700003)
node3.setup_stabiliser(dir_name)

node7 = bioreactor.Node(7)
node7.add_device("PBR", "PBR07", 72700007)
node7.setup_stabiliser(dir_name)

print("Devices ready.")

############ initial setup #############
#node.PBR.set_temp(25)
#node.GMS.set_valve_flow(0, 0.01)
#node.GMS.set_valve_flow(1, 0.33)
#node.GAS.set_flow_target(0.2)
# node1.PBR.set_pwm(50, True)
# node1.PBR.turn_on_light(0, True)
# node1.PBR.turn_on_light(1, True)
# node1.PBR.set_pump_state(5, False)
# node1.PBR.set_temp(25)

node2.PBR.set_pwm(50, True)
node2.PBR.turn_on_light(0, True)
node2.PBR.turn_on_light(1, True)
node2.PBR.set_pump_state(5, False)
#node2.PBR.set_temp(25)

node3.PBR.set_pwm(50, True)
node3.PBR.turn_on_light(0, True)
node3.PBR.turn_on_light(1, True)
node3.PBR.set_pump_state(5, False)
#node3.PBR.set_temp(25)

node7.PBR.set_pwm(50, True)
node7.PBR.turn_on_light(0, True)
node7.PBR.turn_on_light(1, True)
node7.PBR.set_pump_state(5, False)
#node7.PBR.set_temp(25)
########################################

print("Setup done.")

#nodes = [node1, node2, node3]
nodes = [node2, node3, node7]

# multiparametric_space = {params[1]: (100, 800), # red light
# 						 params[2]: (100, 800)} # blue light

multiparametric_space = {params[0]: (15, 35)}

particles = []
swarm_results = []  # important variable shared by all particles (including swarm)

swarm = Swarm(swarm_results, multiparametric_space)

# conditions = [np.array([561, 563]), np.array([211, 164]), np.array([327, 404])]
# conditions = [np.array([211, 164]), np.array([327, 404])]
conditions = [np.array([23]), np.array([26.2]), np.array([24.4])]

n_of_nodes = len(nodes)

for i in range(n_of_nodes):
	random_position = []
	step = random.uniform(0, 1)
	##### JUST TOO KEEP SAME CONDITIONS #######
	# random_position = [200, 232]
	# for key in swarm.parameter_keys:
		# random_position.append(random.uniform(min(multiparametric_space[key]), max(multiparametric_space[key])))
	################################
	particles.append(Particle(conditions[i], step, swarm, nodes[i], dir_name))

print("Swarm created, starting...")

swarm.start()

for particle in particles:
	time.sleep(5)
	particle.start()

while swarm.is_alive():
	pass # we just have to wait until the swarm particle is finished

print("************* Experiment is finishing ***********")

for particle in particles:
	particle.stoprequest.set()

print("\n++++++++++++ OVERALL RESULTS ++++++++++++\n")

values = []
for particle in particles:
	print("------- Results for particle", particle.node.PBR.ID, particle.name)
	print(particle.particle_trace)
	values.append(max(column(1, particle.particle_trace)))
	print("BEST:", values[-1])

print("Actual best:", max(values))
print('Swarm best:', swarm.swarm_best)