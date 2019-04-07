import sys
import time
import datetime

def show_time():
    return str(datetime.datetime.now() + datetime.timedelta(hours=2)) + " | "

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        name = time.strftime("%Y%m%d-%H%M%S")
        self.log = open(".log/" + name + ".log", "a")
        self.new_line = True

    def write(self, message):
        if self.new_line:
            self.terminal.write(show_time() + message)
            self.log.write(show_time() + message)  
            self.new_line = False
        else:
            self.terminal.write(message)
            self.log.write(message) 
        if message == "\n":
            self.new_line = True

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

sys.stdout = Logger()