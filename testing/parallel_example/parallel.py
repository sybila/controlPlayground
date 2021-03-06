import threading
import random
import time


# this is basically the Particle
class Worker(threading.Thread):
    def __init__(self, conditions, results, observer):
        super(Worker, self).__init__()
        self.conditions = conditions
        self.global_results = results
        self.stoprequest = threading.Event()
        self.local_best = ([None, None, None], 0)
        self.history = []
        self.observer = observer

    def run(self):
        while not self.stoprequest.isSet():
            result = self.do_some_computation()
            self.history.append((self.conditions, result))
            self.global_results.append((self.conditions, result))
            if self.local_best[1] < result:
                self.local_best = (self.conditions, result)
            self.conditions = self.compute_new_conditions()

    # let a bioreactor do its stuff
    def do_some_computation(self):
        result = self.conditions[0] ** 3 + self.conditions[1] ** 2 - self.conditions[2]
        print(self.name, "I'm computing:", self.conditions, result)
        time.sleep(random.random())  # to simulate the fact the computation will take some time
        # some random function we are investigating
        return result

    # decide new conditions for the bioreactor
    def compute_new_conditions(self):
        print("Current best: global - ", self.observer.global_best[1], "local - ", self.local_best[1])
        return [random.randint(0, 100) for _ in range(3)]

    def join(self, timeout=None):
        # self.stoprequest.set()
        super(Worker, self).join(timeout)


# an Observer over all threads globally
# workers append their results to shared list
# observer takes them one by one and evaluates them
class Checker(threading.Thread):
    def __init__(self, results):
        super(Checker, self).__init__()
        self.global_results = results
        self.global_best = ([None, None, None], 0)
        self.No_of_results = 0
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            if self.global_results:
                new = self.global_results.pop()
                if new[1] > self.global_best[1]:
                    self.global_best = new
                self.condition_holds()

    def condition_holds(self):
        print("Checker:", self.No_of_results, self.global_best)
        self.No_of_results += 1
        if self.No_of_results > 100:
            self.stoprequest.set()

    def join(self, timeout=None):
        super(Checker, self).join(timeout)
