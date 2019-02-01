import os

DEFINITION_1 = '''
(define '''

DEFINITION_2 = '''
  (make-rpc
   (make-binary-unix-client
	"/tmp/devbus" "'''

DEFINITION_3 = '''")))

(spawn-rendezvous-selector-loop)

'''

class Device():
	def __init__(self, particle, ID, adress):
		self.particle = particle
		self.ID = ID
		self.adress = adress
		self.definition = DEFINITION_1 + ID + DEFINITION_2 + str(adress) + DEFINITION_3
		self.command = ["(print (rpc2 " + ID + " `(", ")))"]
		self.filename = os.getcwd() + '/script.scm'

	def __del__(self):
		try:
			os.remove(self.filename)
		except FileNotFoundError:
			pass

	def __str__(self):
		return self.ID + " @ " + str(self.adress)

	def __repr__(self):
		return "Device(" + self.ID + ", " + str(self.adress) + ")"