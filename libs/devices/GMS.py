import os

DEFINITION = \
'''
(define GMS
  (make-rpc
   (make-binary-unix-client
    "/tmp/devbus" "46700003")))

(spawn-rendezvous-selector-loop)

'''

class GMS():
    def __init__(self):
        self.definition = DEFINITION
        self.command = ["(print (rpc2 GMS `(", ")))"]
        self.filename = os.getcwd() + '/script.scm'

    def __del__(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass