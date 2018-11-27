import os

DEFINITION = \
'''
(define GAS
  (make-rpc
   (make-binary-unix-client
    "/tmp/devbus" "42700007")))

(spawn-rendezvous-selector-loop)

'''

class GAS():
    def __init__(self):
        self.definition = DEFINITION
        self.command = ["(print (rpc2 GAS `(", ")))"]
        self.filename = os.getcwd() + '/script.scm'

    def __del__(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass