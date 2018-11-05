import os

DEFINITION = \
'''
(define PBR07
  (make-rpc
   (make-binary-unix-client
    "/tmp/devbus" "72700007")))

(spawn-rendezvous-selector-loop)

'''

class PBR():
    def __init__(self):
        self.definition = DEFINITION
        self.command = ["(print (rpc2 PBR07 `(", ")))"]
        self.filename = os.getcwd() + '/script.scm'

    def __del__(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass