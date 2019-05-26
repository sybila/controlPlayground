import numpy as np
import csv
import datetime

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .DataHolder import *
from .GrowthChecker import *
from .Regression import *
from bioreactor import logger


class Stabiliser(logger.Logger):
    def __init__(self, node, dir_name, OD_MAX, OD_MIN, TIMEOUT, linear_tol, confidence_tol, max_time=5/3600):
        self.dir_name = dir_name
        self.node = node

        self.OD_MAX = OD_MAX
        self.OD_MIN = OD_MIN
        self.TIMEOUT = TIMEOUT
        self.max_time = max_time * 3600  # to seconds

        self.checker = GrowthChecker(self.node.PBR.ID, self.dir_name, linear_tol, confidence_tol)
        self.holder = DataHolder(self.node.PBR, [OD_MIN, OD_MAX], self.dir_name)

        self.pump = 5

        self.first_max_time = None

        logger.Logger.__init__(self, self.dir_name, self.node.PBR.ID)

    # turns on pump and measured OD in cycle intil it reaches OD_MIN (with some tolerance)
    def pump_out_population(self, pump):
        self.log("Reaching min population...")
        self.holder.device.set_pump_state(pump, True)
        while self.holder.next_value() > self.OD_MIN:
            if self.node.stop_working:
                return
            if self.reached_max_time():
                return
            time.sleep(self.TIMEOUT)
        self.holder.device.set_pump_state(pump, False)
        self.log("Min pupulation reached.")

    # given a PBR, it checks in cycle the OD every n seconds, once OD_MAX is reached it
    # calculates current growth rate using measured OD data and exponentional regression
    # has to remember initial OD!
    def reach_max_population(self):
        self.log("Reaching max population...")
        while self.holder.next_value() < self.OD_MAX:
            if self.node.stop_working:
                return
            if self.reached_max_time():
                return
            time.sleep(self.TIMEOUT)
        if not self.first_max_time:
            self.first_max_time = time.time()
        self.log("Max population reached:\n",
                 "times = ", self.holder.times,
                 "\n data = ", self.holder.data)
        r = exponentional_regression(self.holder.times[1:], self.holder.data[1:], self.holder.data[1])
        return r if r > 0 else 0

    # it is called when we start with new conditions
    # and they are all set for given node
    # assume conditions has form [temp, co2-flow, intensity]
    def set_up_conditions(self, conditions, parameter_keys):
        funcs = {"temp": self.node.PBR.set_temp,
                 "light-red": lambda intensity: self.node.PBR.set_light_intensity(0, intensity),
                 "light-blue": lambda intensity: self.node.PBR.set_light_intensity(1, intensity),
                 "flow": lambda co2_flow: self.node.GMS.set_valve_flow(0, co2_flow)}
        success = []
        for i in range(len(parameter_keys)):
            if type(conditions[i]) == list:
                success.append(funcs[parameter_keys[i]](*conditions[i]))
            else:
                success.append(funcs[parameter_keys[i]](conditions[i]))
        return all(success)

    def get_growth_rate(self, conditions, parameter_keys, history_len=5):
        self.history_len = history_len
        self.holder.restart()
        self.checker.restart()
        try:
            self.log("Measuring growth rate...")
            self.set_up_conditions(conditions, parameter_keys)
            self.log("Prepared given conditions.")
            self.log("Computing initial OD average...")
            self.holder.measure_initial_OD()
            self.log("Initial OD average:", self.holder.average)
            self.holder.set_init_time(time.time())
            self.log("Starting...")

            while not self.checker.is_stable(self.history_len):
                if self.reached_max_time():
                    if self.checker.values:
                        avg = np.mean(self.checker.values[-self.history_len:])
                    else:
                        avg = np.inf
                    self.log("Max time", self.max_time/3600, "hours exceeded - returning average ", avg)
                    save(self.holder, self.checker, self.history_len, self.dir_name, self.node.PBR.ID, conditions)
                    return avg
                self.log("Iteration", len(self.checker.values))
                self.pump_out_population(self.pump)
                if self.node.stop_working:
                    return
                self.holder.reset()
                value = self.reach_max_population()
                if self.node.stop_working:
                    return
                if value:
                    doubling_time = (np.log(2) / value)
                    self.log("New growth rate:", value, "(Doubling time:", doubling_time / 3600, "h)")
                    self.checker.values.append(doubling_time)
                    self.checker.times.append((time.time() - self.holder.init_time))
                    self.holder.reset(value)

            self.log("All data measured for this conditions:\n",
                     "times:", self.holder.time_history,
                     "\n data:", self.holder.data_history)

            save(self.holder, self.checker, self.history_len, self.dir_name, self.node.PBR.ID, conditions)
        except Exception as e:
            self.log_error(e)
        if self.checker.values:
            return self.checker.values[-1]  # which should be stable
        self.log("lets return inf")
        return np.inf

    def reached_max_time(self):
        if time.time() - self.holder.init_time > self.max_time:
            if self.first_max_time:
                if time.time() - self.first_max_time > self.max_time:
                    return True
                return False
            return True
        return False


# saves data in svg and creates a picture
def save(holder, checker, history_len, dir_name, ID, conditions):
    current_time = '{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now() + datetime.timedelta(hours=2))
    rows = []
    fig, ax1 = plt.subplots()

    plt.title(ID + " Stable doubling time " + "%.2f" % (checker.values[-1]/3600) + " h" +
              "\n for conditions " + str(conditions))

    rows += list(map(lambda t, v: (t, v, None, None, None), holder.time_history, holder.data_history))
    # raw OD data
    ax1.plot(to_hours(holder.time_history), holder.data_history, 'o', markersize=2)
    ax1.set_xlabel('time (h)')
    ax1.set_ylabel('OD')
    ax1.yaxis.label.set_color('blue')

    # exponencial regression of OD regions
    for data in holder.reg_history:
        times = np.linspace(data["start"], data["end"], 1000)
        values = data["n_0"] * np.exp((times - data["start"]) * data["rate"])
        ax1.plot(to_hours(times), values, '-b')
        rows += list(map(lambda t, v: (t, None, None, v, None), times, values))

    # checker's data
    ax2 = ax1.twinx()
    ax2.set_ylabel('doubling time (h)')
    ax2.plot(to_hours(checker.times), to_hours(checker.values), 'or')
    ax2.yaxis.label.set_color('red')

    rows += list(map(lambda t, v: (t, None, v, None, None), checker.times, checker.values))

    # measured doubling times
    coeffs = linear_regression(checker.times[-history_len:], checker.values[-history_len:])
    times = np.linspace(checker.times[-history_len], checker.times[-1], 500)
    values = coeffs[1] + coeffs[0] * times
    ax2.plot(to_hours(times), to_hours(values), '-r')

    rows += list(map(lambda t, v: (t, None, None, None, v), times, values))

    fig.tight_layout()
    plt.savefig(dir_name + "/" + ID + "/" + ID + "_" + current_time + "_fig.png", dpi=150)

    save_csv(rows, dir_name, ID, current_time)


def save_csv(rows, dir_name, ID, current_time):
    rows.sort(key=lambda x: x[0])
    with open(dir_name + "/" + ID + "/" + current_time + '_OD.csv', mode='w') as file:
        row_writer = csv.writer(file, delimiter=',')
        row_writer.writerow(["time", "OD", "doubling time", "expo regression", "lin regression"])
        for row in rows:
            row_writer.writerow(row)


def to_hours(times):
    return np.array(times) / 3600
