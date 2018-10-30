import subprocess
import time
import os, re, sys

sys.path.append(os.path.abspath('devices/'))
import GMS as GasMixer
import PBR as Bioreactor

sys.path.append(os.path.abspath('connection/'))
import connection as SSH

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

USER = 'root'
FOLDER = '/root/control/'
SERVER = '192.168.17.13'

def write_scm_file(device, value, args=[]):
    '''
    Creates a Scheme script by composing HEADER and COMMAND constants with given arguments
    '''
    with open(device.filename, 'w') as file:
        file.write(HEADER)
        file.write(device.definition)
        file.write(device.command[0] + value + " " + " ".join(map(str, args)) + device.command[1])

def execute(transfer, device, value, args=[]):
    '''
    Reads output from bioreactor by calling a Scheme script
    '''
    write_scm_file(device, value, args)

    transfer.put(device.filename, FOLDER + os.path.basename(device.filename))
    ssh_stdin, ssh_stdout, ssh_stderr = \
            transfer.execute_cmd("gosh " + FOLDER + re.escape(os.path.basename(device.filename)))

    if ssh_stderr.readlines():
        print(ssh_stderr.readlines())
    output = ssh_stdout.readlines()

    return output

# while True:
#     print(get_output())
#     time.sleep(2)

# --------------------------------------------------------------
# API

PBR = Bioreactor.PBR()
GMS = GasMixer.GMS()
transfer = SSH.SSHconnection(SERVER, USER)

# Temperature

def get_temp_settings():
    return execute(transfer, PBR, "get-thermoregulator-settings")

def get_temp():
    try:
        return float(execute(transfer, PBR, "get-current-temperature")[0])
    except Exception:
        return None

def set_temp(temp):
    try:
        return execute(transfer, PBR, "set-thermoregulator-temp", [temp])[0].rstrip() == 'ok'
    except Exception:
        return False

# pH 

def get_ph():
    try:
        return float(execute(transfer, PBR, "get-ph", [5, 0])[0])
    except Exception:
        return None

# valve

def get_valve_flow(valve):
    return execute(transfer, GMS, "get-valve-flow", [valve])

def get_mode():
    return execute(transfer, GMS, "get-mode")
