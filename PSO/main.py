import numpy as np
import random
import os, sys
import datetime
import time
import shutil

from Particle import *
from Swarm import *
import bioreactor
from prompt import prompt

params = ["temp", "light-red", "light-blue", "flow"]

print("Initial setup...")

########## TESTING ########
# TIMEOUT = 0.001
# conf_tol = 0.99
# MAX_VALUES = 5
# TESTING = True

# OD_MIN = 0.43
# OD_MAX = 0.47
####### EXPERIMENTS #######
TIMEOUT = 60
conf_tol = 0.06
MAX_VALUES = 100
TESTING = False

OD_MIN = 0.43
OD_MAX = 0.47
###########################

now = datetime.datetime.now() + datetime.timedelta(hours=2)
log_name = ".log/" + '{:%Y%m%d-%H%M%S}'.format(now)
working_dir =  ".log/RUNNING"

if os.path.exists(working_dir):
	name = datetime.datetime.fromtimestamp(os.path.getctime(working_dir)) + datetime.timedelta(hours=2)
	os.rename(working_dir, '.log/' + '{:%Y%m%d-%H%M%S}'.format(name))

os.mkdir(working_dir)

####### setup nodes ########

nodes = []

nodes.append(bioreactor.Node(TESTING))
nodes[-1].add_device("PBR", "PBR01", 72700001)

nodes.append(bioreactor.Node(TESTING))
nodes[-1].add_device("PBR", "PBR02", 72700002)

nodes.append(bioreactor.Node(TESTING))
nodes[-1].add_device("PBR", "PBR03", 72700003)

nodes.append(bioreactor.Node(TESTING))
nodes[-1].add_device("PBR", "PBR04", 72700004)

print("Devices ready.")

############ initial setup #############

for node in nodes:
	os.mkdir(working_dir + "/" + node.PBR.ID)
	node.setup_stabiliser(OD_MIN, OD_MAX, TIMEOUT, confidence_tol=conf_tol)
	node.PBR.set_thermoregulator_state(1)
	node.PBR.set_pwm(50, True)
	node.PBR.turn_on_light(0, True)
	node.PBR.turn_on_light(1, True)
	node.PBR.set_pump_state(5, False)
	node.PBR.set_light_intensity(0, 60)
	node.PBR.set_light_intensity(1, 30)

########################################

print("Setup done.")

# multiparametric_space = {params[1]: (100, 800), # red light
# 						 params[2]: (100, 800)} # blue light

multiparametric_space = {params[0]: (15, 40)}

print("Creating and starting swarm...")

swarm = Swarm(multiparametric_space, MAX_VALUES)
swarm.type = -1
swarm.start()

# conditions = [np.array([561, 563]), np.array([211, 164]), np.array([327, 404])]
conditions = [np.array([24]), np.array([20]), np.array([26]), np.array([30])]

for i in range(len(nodes)):
	step = random.uniform(0, 1)
	##### choose random position #######
	# random_position = []
	# for key in swarm.parameter_keys:
		# random_position.append(random.uniform(min(multiparametric_space[key]), max(multiparametric_space[key])))
	################################
	time.sleep(5)
	swarm.add_particle(Particle(conditions[i], step, swarm, nodes[i]))

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

swarm.exit()

print("Experiment finished.")
print('Swarm best:', swarm.swarm_best)

swarm.save()

# rename working_dir to log_name
os.rename(working_dir, log_name)