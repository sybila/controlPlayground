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
	data = xml.read_xml(sys.argv[-1])
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

multiparametric_space = dict()
swarm_keys = []

for parameter in data['settings']['parameter_space'].items():
		swarm_keys.append(parameter[0])
		multiparametric_space[parameter[0]] = list(map(float, parameter[1]))

swarm = Swarm(multiparametric_space, int(data['settings']['max_values']), swarm_keys, dir_name=working_dir)
swarm.type = int(data['settings']['optimum_type'])
swarm.start()

for node in data['nodes']:
	particle = import_particle(node, swarm, working_dir, data, write=False)
	time.sleep(2)
	swarm.add_particle(particle)

########################################

print("Setup done.")

xml.write_xml(data, working_dir)

while swarm.is_alive():
	try:
		user_input = prompt.command(globals())
		try:
			exec(user_input)
		except Exception as e:
			raise(e)
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