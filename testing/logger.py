import sys
import time


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        name = time.strftime("%Y%m%d-%H%M%S")
        self.log = open(".log/" + name + ".log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


sys.stdout = Logger()
