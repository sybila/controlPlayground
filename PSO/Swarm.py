import threading
import numpy as np
import csv
import time

import matplotlib

matplotlib.use('Agg')
matplotlib.rc('figure', max_open_warning=0)
import matplotlib.pyplot as plt

import bioreactor

COLOURS = "bgrcmyk"


# an Observer over all threads globally
# workers append their results to shared list
# observer takes them one by one and evaluates them
class Swarm(threading.Thread):
    def __init__(self, multiparametric_space, max_values, parameter_keys, dir_name=".log/RUNNING", optimum_type=-1):
        super(Swarm, self).__init__()

        self.optimum_type = optimum_type  # optimum type, -1 for min
        self.swarm_results = []
        self.parameter_keys = parameter_keys
        self.boundaries = self.create_boundaries(multiparametric_space)
        self.No_of_results = 0
        self.stoprequest = threading.Event()
        self.log = open(dir_name + "/history.log", "a")
        self.dir_name = dir_name
        self.particles = []
        self.MAX_VALUES = max_values

    def run(self):
        while not self.stoprequest.isSet():
            if self.swarm_results:
                new_value = self.swarm_results.pop(0)
                if new_value[1] * self.optimum_type > self.swarm_best[1] * self.optimum_type:
                    self.swarm_best = new_value
                self.condition_holds()
        self.quit_particles()

    def condition_holds(self):
        self.log.write(bioreactor.show_time() + "Swarm best so far: No " +
                       str(self.No_of_results) + ", best: " + str(self.swarm_best) + "\n")
        self.log.flush()
        self.No_of_results += 1
        if self.No_of_results > self.MAX_VALUES:
            self.stoprequest.set()

    def join(self, timeout=None):
        super(Swarm, self).join(timeout)

    def create_boundaries(self, space):
        self.swarm_best = []
        boundaries = [[], []]
        for key in self.parameter_keys:
            boundaries[0].append(space[key][0])
            boundaries[1].append(space[key][1])
            self.swarm_best.append(sum(boundaries[-1]) / 2)
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

    def quit_particles(self):
        for particle in self.particles:
            particle.exit()

    def exit(self):
        self.stoprequest.set()
        while any([p.is_alive() for p in self.particles]):
            time.sleep(5)
        time.sleep(2)

    def export_data(self):
        self.rows = []
        self.header = list(self.parameter_keys)
        n_params = len(self.parameter_keys)
        n_particles = len(self.particles)
        for i, particle in enumerate(self.particles):
            self.header.append(particle.node.PBR.ID)
            for point in particle.particle_trace:
                row = [None] * (n_particles + n_params)
                row[0:n_params] = point[0]
                row[i + n_params] = point[1]
                self.rows.append(row)

        self.rows = np.array(self.rows)

    def save(self):
        self.export_data()
        self.save_csv()
        self.save_plot()

    def save_csv(self, filename='results.csv'):
        with open(self.dir_name + '/' + filename, mode='w') as file:
            row_writer = csv.writer(file, delimiter=',')
            row_writer.writerow(self.header)
            for row in self.rows:
                row_writer.writerow(row)

    def save_plot(self, filename='results.png'):
        param_names = list(self.parameter_keys)
        if len(self.rows) != 0:
            colours = plt.cm.rainbow(np.linspace(0, 1, len(self.rows[0]) - len(param_names)))
            for j in range(len(param_names)):
                f, ax = plt.subplots()
                for i in range(len(param_names), len(self.rows[0])):
                    params = self.rows[:, j]
                    ODs = self.rows[:, i]
                    values = np.array(list(filter(lambda v: v[1] is not None, zip(params, ODs))))
                    if values.size != 0:
                        params = values[:, 0]
                        ODs = values[:, 1]
                        ID = self.header[i]
                        ax.plot(params, ODs, ',', color=colours[i - len(param_names)])
                        ax.quiver(params[:-1], ODs[:-1], params[1:]-params[:-1], ODs[1:]-ODs[:-1],
                                  scale_units='xy', angles='xy', scale=1, color=colours[i - len(param_names)], label=ID)

                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

                legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), shadow=True)

                plt.savefig(self.dir_name + '/' + param_names[j] + "_" + filename, dpi=150)
