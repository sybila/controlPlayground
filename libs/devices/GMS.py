class GMS():
	def __init__(self):
		self.definition = \
				'''
				(define GMS
				  (make-rpc
				   (make-binary-unix-client
				    "/tmp/devbus" "46700003")))

				(spawn-rendezvous-selector-loop)

				'''
		self.command = ["(print (rpc2 GMS `(", ")))"]
		self.filename = 'scm_scripts/script.scm'