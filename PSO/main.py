import numpy as np
import random
import os, sys
import datetime
import time

from Particle import *
from Swarm import *
import bioreactor
from prompt import prompt

params = ["temp", "light-red", "light-blue", "flow"]

print("Initial setup...")

now =  datetime.datetime.now() + datetime.timedelta(hours=2)
dir_name = ".log/" + '{:%Y%m%d-%H%M%S}'.format(now)
# dir_name =  ".log/TESTING" # for testing
os.mkdir(dir_name)

node_IDs = ["PBR02", "PBR03", "PBR07"]

for ID in node_IDs:
	os.mkdir(dir_name + "/" + ID)

####### setup nodes ########

nodes = []

nodes.append(bioreactor.Node(2))
nodes[-1].add_device("PBR", "PBR02", 72700002)
nodes[-1].setup_stabiliser(dir_name)

nodes.append(bioreactor.Node(3))
nodes[-1].add_device("PBR", "PBR03", 72700003)
nodes[-1].setup_stabiliser(dir_name)

nodes.append(bioreactor.Node(7))
nodes[-1].add_device("PBR", "PBR07", 72700007)
nodes[-1].setup_stabiliser(dir_name)

print("Devices ready.")

############ initial setup #############

nodes[-1].PBR.set_pwm(50, True)
nodes[-1].PBR.turn_on_light(0, True)
nodes[-1].PBR.turn_on_light(1, True)
nodes[-1].PBR.set_pump_state(5, False)
nodes[-1].PBR.set_light_intensity(0, 200)
nodes[-1].PBR.set_light_intensity(1, 150)

nodes[-1].PBR.set_pwm(50, True)
nodes[-1].PBR.turn_on_light(0, True)
nodes[-1].PBR.turn_on_light(1, True)
nodes[-1].PBR.set_pump_state(5, False)
nodes[-1].PBR.set_light_intensity(0, 200)
nodes[-1].PBR.set_light_intensity(1, 150)

nodes[-1].PBR.set_pwm(50, True)
nodes[-1].PBR.turn_on_light(0, True)
nodes[-1].PBR.turn_on_light(1, True)
nodes[-1].PBR.set_pump_state(5, False)
nodes[-1].PBR.set_light_intensity(0, 200)
nodes[-1].PBR.set_light_intensity(1, 150)

########################################

print("Setup done.")

# multiparametric_space = {params[1]: (100, 800), # red light
# 						 params[2]: (100, 800)} # blue light

multiparametric_space = {params[0]: (15, 35)}

print("Creating and starting swarm...")

swarm = Swarm(multiparametric_space, dir_name)
swarm.type = -1
swarm.start()

# conditions = [np.array([561, 563]), np.array([211, 164]), np.array([327, 404])]
conditions = [np.array([21]), np.array([25]), np.array([29])]

for i in range(len(nodes)):
	step = random.uniform(0, 1)
	##### choose random position #######
	# random_position = []
	# for key in swarm.parameter_keys:
		# random_position.append(random.uniform(min(multiparametric_space[key]), max(multiparametric_space[key])))
	################################
	time.sleep(5)
	swarm.add_particle(Particle(conditions[i], step, swarm, nodes[i], dir_name))

print("Swarm started.")

while swarm.is_alive():
	try:
		user_input = prompt.command(globals())
		try:
			exec(user_input)
		except Exception as e:
			print(e)
	except KeyboardInterrupt as e:
		print("Type exit() to quit the interpreter.\nType swarm.exit() or press Ctrl+D to end the experiment.")
	except EOFError as e:
		swarm.exit()
		time.sleep(5)

swarm.exit()

print("Experiment finished.")
print('Swarm best:', swarm.swarm_best)

swarm.save()