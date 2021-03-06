import os, re

from .devices import GAS
from .stabilisation import Stabiliser

HEADER = \
    '''#!/usr/bin/env gosh

    (use util.match)
    (use sad.channel3-rv)
    (use sad.gauche)
    (use srfi-19)
    (use sad.rendezvous)
    (use sad.binary-channels)
    (use util.list)
    (use gauche.threads)
    (use sad.regression)

    '''


class Node():
    def __init__(self, testing=False, user='root', folder='/root/control/', server='192.168.17.13'):
        self.folder = folder
        self.devices = []
        self.stop_working = False
        if testing:
            from .devices import PBR_test as PBR
            from .devices import GMS_test as GMS
            from .devices import SSHconnection
        else:
            from .devices import PBR
            from .devices import GMS
            from .connection import SSHconnection
        self.connection = SSHconnection(server, user)
        self.types = {"PBR": PBR, "GMS": GMS, "GAS": GAS}

    def setup_stabiliser(self, OD_MIN, OD_MAX, TIMEOUT=1, linear_tol=0.04, confidence_tol=0.06,
                         dir_name=".log/RUNNING"):
        self.stabiliser = Stabiliser(self, dir_name, OD_MAX, OD_MIN, TIMEOUT, linear_tol, confidence_tol)

    def add_device(self, name, ID, adress):
        setattr(self, name, self.types[name](self, ID, adress))
        self.devices.append(name)

    def write_scm_file(self, device, value, args=[]):
        '''
        Creates a Scheme script by composing HEADER and COMMAND constants with given arguments
        '''
        with open(device.filename, 'w') as file:
            file.write(HEADER)
            file.write(device.definition)
            file.write(device.command[0] + value + " " + " ".join(map(str, args)) + device.command[1])

    def execute(self, device, value, args=[]):
        '''
        Reads output from bioreactor by calling a Scheme script
        '''
        self.write_scm_file(device, value, args)

        self.connection.put(device.filename, self.folder + os.path.basename(device.filename))
        ssh_stdin, ssh_stdout, ssh_stderr = \
            self.connection.execute_cmd("gosh " + self.folder + re.escape(os.path.basename(device.filename)))


        stderr = ssh_stderr.readlines()
        if stderr:
            print(stderr)
        output = ssh_stdout.readlines()

        return output

    def stabilise(self, conditions, parameter_keys):
        return self.stabiliser.get_growth_rate(conditions, parameter_keys)
