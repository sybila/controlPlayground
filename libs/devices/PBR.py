class PBR():
	def __init__(self):
		self.definition = \
				'''
				(define PBR07
				  (make-rpc
				   (make-binary-unix-client
				    "/tmp/devbus" "72700008")))

				(spawn-rendezvous-selector-loop)

				'''
		self.command = ["(print (rpc2 PBR07 `(", ")))"]
		self.filename = 'scm_scripts/script.scm'