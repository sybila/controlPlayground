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
from parsing import xml_parse as xml

###########################
print("Initial setup...")

if len(sys.argv) > 1:
	data = xml.parse(sys.argv[-1])
else:
	from settings import data

###########################
# prepare folders

now = datetime.datetime.now() + datetime.timedelta(hours=2)
log_name = ".log/" + '{:%Y%m%d-%H%M%S}'.format(now)
working_dir = data['settings']['working_dir']

if os.path.exists(working_dir):
	name = datetime.datetime.fromtimestamp(os.path.getctime(working_dir)) + datetime.timedelta(hours=2)
	os.rename(working_dir, '.log/' + '{:%Y%m%d-%H%M%S}'.format(name))

os.mkdir(working_dir)

###########################
# setup nodes
print("Preparing devices...")

nodes = []
multiparametric_space = dict()
swarm_keys = []

for parameter in data['settings']['parameter_space'].items():
		swarm_keys.append(parameter[0])
		multiparametric_space[parameter[0]] = eval(parameter[1])

swarm = Swarm(multiparametric_space, int(data['settings']['max_values']), swarm_keys, dir_name=working_dir)
swarm.type = int(data['settings']['optimum_type'])
swarm.start()

for node in data['nodes'].values():
	nodes.append(bioreactor.Node(bool(data['settings']['testing'])))
	for device in node['devices'].values():
		nodes[-1].add_device(device['name'], device['ID'], int(device['adress']))
		for command in device['initial_setup'].values():
			args = ", ".join(command['arguments'].values())
			eval('nodes[-1].' + device['name'] + '.' + command['command'] + '(' + args + ')')

	os.mkdir(working_dir + "/" + nodes[-1].PBR.ID)
	nodes[-1].setup_stabiliser(float(data['settings']['OD_MIN']),
						  float(data['settings']['OD_MIN']),
						  int(data['settings']['timeout']),
						  linear_tol=float(data['settings']['lin_tol']),
						  confidence_tol=float(data['settings']['conf_tol']),
						  dir_name=working_dir)

	step = random.uniform(0, 1)
	conditions = eval(node['parameter_values'])
	time.sleep(2)
	swarm.add_particle(Particle(conditions, step, swarm, nodes[-1], dir_name=working_dir))

########################################

print("Setup done.")

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