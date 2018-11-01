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
CONNECTION = SSH.SSHconnection(SERVER, USER)
GAS_TYPES = ["CO2", "Air", "N2"]

def write_scm_file(device, value, args=[]):
    '''
    Creates a Scheme script by composing HEADER and COMMAND constants with given arguments
    '''
    with open(device.filename, 'w') as file:
        file.write(HEADER)
        file.write(device.definition)
        file.write(device.command[0] + value + " " + " ".join(map(str, args)) + device.command[1])

def execute(device, value, args=[]):
    '''
    Reads output from bioreactor by calling a Scheme script
    '''
    write_scm_file(device, value, args)

    CONNECTION.put(device.filename, FOLDER + os.path.basename(device.filename))
    ssh_stdin, ssh_stdout, ssh_stderr = \
            CONNECTION.execute_cmd("gosh " + FOLDER + re.escape(os.path.basename(device.filename)))

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

# Temperature

def get_temp_settings():
    '''
    Get information about currently set temperature, maximal and
    minimal allowed temperature.
    '''
    results = ["set", "min", "max"]
    try:
        values = execute(PBR, "get-thermoregulator-settings")[0].rstrip()[1:-1].split()
    except Exception:
        return None
    return dict(zip(results, list(map(float, values[1:-1]))))

def get_temp():
    '''
    Get current temperature.
    '''
    try:
        return float(execute(PBR, "get-current-temperature")[0])
    except Exception:
        return None

def set_temp(temp):
    '''
    Set desired temperature.
    '''
    try:
        return execute(PBR, "set-thermoregulator-temp", [temp])[0].rstrip() == 'ok'
    except Exception:
        return False

# pH 

def get_ph():
    '''
    Get current pH.
    '''
    try:
        return float(execute(PBR, "get-ph", [5, 0])[0])
    except Exception:
        return None

# valve

def get_valve_flow(valve):
    '''
    Get current flow in the given valve. 
    '''
    results = ["current", "set"]
    try:
        values = execute(GMS, "get-valve-flow", [valve])[0].rstrip()[1:-1].split()
    except Exception:
        return None
    return dict(zip(results, list(map(float, values[1:-1]))))
    '''
    Set flow to value for the given valve. 
    '''
def set_valve_flow(valve, value):
    try:
        return execute(GMS, "set-valve-tflow", [valve, value])[0].rstrip() == 'ok'
    except Exception:
        return None

def get_valve_info(valve):
    '''
    Gives information about the valve
    Returns a dictionary with gas type and maximal allowed flow.
    '''
    results = ["max_flow", "gas_type"]
    values = [None, None]
    try:
        values = execute(GMS, "get-valve-info", [valve])[0].rstrip()[1:-1].split()
    except Exception:
        return None
    return dict(zip(results, [float(values[1]), GAS_TYPES[int(values[3])]]))