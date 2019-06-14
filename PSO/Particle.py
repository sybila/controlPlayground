import threading
import random
import time
import os
import numpy as np
from scipy import interpolate
from parsing import xml_parse as xml

import bioreactor


class Particle(threading.Thread, bioreactor.Logger):
    def __init__(self, position, step, observer, node, dir_name=".log/RUNNING", cognitive_parameter=0.3,
                 social_parameter=0.5, inertia_weight=0.4):
        threading.Thread.__init__(self)
        self.position = position
        self.step = step

        self.observer = observer
        self.node = node
        self.dir_name = dir_name

        bioreactor.Logger.__init__(self, dir_name, node.PBR.ID)

        self.particle_best = (position, self.observer.optimum_type * np.inf * (-1))
        self.particle_trace = []

        self.cognitive_parameter = cognitive_parameter
        self.social_parameter = social_parameter
        self.inertia_weight = inertia_weight

        self.max_step = 1/5
        self.pump = 5

        self.stoprequest = threading.Event()

    def __str__(self):
        return str(self.node.PBR.ID)

    def __repr__(self):
        return "Particle({0})".format(self.node.PBR.ID)

    def run(self):
        while not self.stoprequest.isSet():
            self.log("_" * 30, "\nI'm computing:\n", list(zip(self.observer.parameter_keys, self.position)))
            result = self.compute_cost_function()
            if self.node.stop_working:
                continue
            self.log("I have computed:", result, "for conditions:\n", list(zip(self.observer.parameter_keys, self.position)))
            if result == np.inf:
                result = self.observer.optimum_type * np.inf * (-1)

            self.particle_trace.append((self.position, result))
            self.observer.swarm_results.append((self.position, result))
            time.sleep(1)
            if result * self.observer.optimum_type > self.particle_best[1] * self.observer.optimum_type:
                self.particle_best = (self.position, result)
            self.position = self.next_position()

    # let a bioreactor do its stuff
    def compute_cost_function(self):
        return self.node.stabilise(self.position, self.observer.parameter_keys)

    # decide new position for the bioreactor
    def next_position(self):
        new_position = self.position + self.inertia_weight * self.step + \
                       self.cognitive_parameter * random.random() * (self.particle_best[0] - self.position) + \
                       self.social_parameter * random.random() * (self.observer.swarm_best[0] - self.position)
        return self.check_boundaries(new_position)

    def check_boundaries(self, new_position):
        smaller_than_min = new_position < self.observer.boundaries[0]
        greater_than_max = new_position > self.observer.boundaries[1]
        for i in range(len(smaller_than_min)):
            if smaller_than_min[i]:
                new_position[i] = self.observer.boundaries[0][i]
        for i in range(len(greater_than_max)):
            if greater_than_max[i]:
                new_position[i] = self.observer.boundaries[1][i]
        return self.check_max_step(new_position)

    def check_max_step(self, new_position):
        differencies = self.position - new_position
        max_steps = (np.array(self.observer.boundaries[1]) - np.array(self.observer.boundaries[0])) * self.max_step
        for i in range(len(differencies)):
            if abs(differencies[i]) > max_steps[i]:
                new_position[i] = (self.position[i] + max_steps[i]) if differencies[i] < 0 else (self.position[i] - max_steps[i])
        return new_position

    def join(self, timeout=None):
        super(Particle, self).join(timeout)

    def exit(self):
        self.node.stop_working = True
        self.stoprequest.set()
        while self.is_alive():
            time.sleep(2)
        self.node.PBR.set_pump_state(self.pump, False)
        self.log("Particle interrupted, bye sweet world!")

    def change_position(self):
        self.log("Forcing the position change manually.")
        self.node.stabiliser.max_time = 0

def import_particle(definition, swarm, working_dir, data, write=True):
    if not isinstance(definition, dict):
        definition = xml.read_xml(definition)

    node = bioreactor.Node(bool(data['settings']['testing']))
    for device in definition['devices']:
        node.add_device(device['name'], device['ID'], int(device['adress']))
        for command in device['initial_setup']:
            args = ", ".join(list(map(str, command['arguments'])))
            eval('node.' + device['name'] + '.' + command['command'] + '(' + args + ')')

    os.mkdir(working_dir + "/" + node.PBR.ID)
    node.setup_stabiliser(float(data['settings']['OD_MIN']),
                          float(data['settings']['OD_MAX']),
                          float(data['settings']['timeout']),
                          linear_tol=float(data['settings']['lin_tol']),
                          confidence_tol=float(data['settings']['conf_tol']),
                          dir_name=working_dir)

    step = random.uniform(0, 1)
    conditions = np.array(list(map(float, definition['parameter_values'])))
    if write:
        data['nodes'].append(definition)
        xml.write_xml(data, working_dir)
    return Particle(conditions, step, swarm, node, dir_name=working_dir)
