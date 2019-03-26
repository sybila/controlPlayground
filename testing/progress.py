import sys

class Progressbar():
	def __init__(self, maximum):
		self.maximum = maximum

	def printProgress(self, progress):
		sys.stdout.write('\r[{0:10}] {1}%'.format('#'*int((progress/self.maximum)*10), int((progress/self.maximum)*100)))
		sys.stdout.flush()