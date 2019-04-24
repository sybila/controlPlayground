import datetime
import os

def show_time():
	return str(datetime.datetime.now() + datetime.timedelta(hours=2)) + " | "

class Logger():
	def __init__(self, dir_name, ID):
		self.ID = ID
		self.global_log = open(dir_name + "/history.log", "a")
		self.local_log  = open(dir_name + "/" + ID + "/history.log", "a")

	def log(self, *args):
		self.write(self.message(args))
		print(self.message(args), end="")

	def log_error(self, error_text):
		self.write(self.error(error_text))
		print(self.error(error_text), end="")

	def write(self, text):
		self.global_log.write(text)
		self.global_log.flush()
		self.local_log.write(text)
		self.local_log.flush()

	def message(self, *args):
		return show_time() + "(" + self.ID + ") " + " ".join(map(str, *args)) + "\n"

	def error(self, error_text):
		return show_time() + "(" + self.ID + ") ERROR: " + str(error_text) + "\n"