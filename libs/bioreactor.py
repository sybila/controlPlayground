import subprocess
import time
import os, re, sys
from paramiko import SSHClient
from scp import SCPClient

sys.path.append(os.path.abspath('devices/'))
import GMS as GasMixer
import PBR as Bioreactor

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


def execute(device, value, args=[]):
    '''
    Reads output from bioreactor by calling a Scheme script
    '''

    write_scm_file(device, value, args)

    ssh = SSHClient() 
    ssh.load_system_host_keys()
    ssh.connect(SERVER, username=USER)

    sftp = ssh.open_sftp()
    sftp.put(device.filename, FOLDER + os.path.basename(device.filename))

    ssh_stdin, ssh_stdout, ssh_stderr = \
            ssh.exec_command("gosh " + FOLDER + re.escape(os.path.basename(device.filename)))

    output = ssh_stdout.readlines()

    sftp.close()
    ssh.close()

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
    return execute(PBR, "get-thermoregulator-settings")

def get_temp():
    try:
        return float(execute(PBR, "get-current-temperature")[0])
    except Exception:
        return None

def set_temp(temp):
    try:
        return execute(PBR, "set-thermoregulator-temp", [temp])[0].rstrip() == 'ok'
    except Exception:
        return False

# pH 

def get_ph():
    try:
        return float(execute(PBR, "get-ph", [5, 0])[0])
    except Exception:
        return None

# valve

def get_valve_flow(valve):
    return execute(GMS, "get-valve-flow", [valve])

def get_mode():
    return execute(GMS, "get-mode")

#print(get_temp_settings())
#print(set_temp(20))
#print(get_temp_settings())