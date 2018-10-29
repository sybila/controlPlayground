import subprocess
import time
import os, re
from paramiko import SSHClient
from scp import SCPClient

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

(define PBR07
  (make-rpc
   (make-binary-unix-client
    "/tmp/devbus" "72700008")))

(spawn-rendezvous-selector-loop)

'''

COMMAND = ["(print (rpc2 PBR07 `(", ")))"]

GET = 'scm_scripts/get_values.scm'
SET = 'scm_scripts/set_values.scm'
USER = 'root'
FOLDER = '/root/control/'
SERVER = '192.168.17.13'

def write_scm_file(file, value, args=[]):
    '''
    Creates a Scheme script by composing HEADER and COMMAND constants with given arguments
    '''
    with open(file, 'w') as file:
        file.write(HEADER)
        file.write(COMMAND[0] + value + " " + " ".join(map(str, args)) + COMMAND[1])


def get_output(value, args=[]):
    '''
    Reads output from bioreactor by calling a Scheme script
    '''

    write_scm_file(GET, value, args)

    ssh = SSHClient() 
    ssh.load_system_host_keys()
    ssh.connect(SERVER, username=USER)

    sftp = ssh.open_sftp()
    sftp.put(GET, FOLDER + os.path.basename(GET))

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("gosh " + FOLDER + re.escape(os.path.basename(GET)))

    output = ssh_stdout.readlines()

    sftp.close()
    ssh.close()

    return output


def set_input(value, args=[]):
    '''
    Sets particular <input> for bioreactor to <value> 
    Requires definition of possible inputs.
    '''

    write_scm_file(SET, value, args)

    ssh = SSHClient() 
    ssh.load_system_host_keys()
    ssh.connect(SERVER, username=USER)

    sftp = ssh.open_sftp()
    sftp.put(SET, FOLDER + os.path.basename(SET))

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("gosh " + FOLDER + re.escape(os.path.basename(SET)))

    output = ssh_stdout.readlines()

    sftp.close()
    ssh.close()

    return output

# while True:
#     print(get_output())
#     time.sleep(2)

# --------------------------------------------------------------
# API

def get_temp():
    try:
        return float(get_output("get-current-temperature")[0])
    except Exception:
        return None

def get_ph():
    try:
        return float(get_output("get-ph", [5, 0])[0])
    except Exception:
        return None

def get_temp_settings():
    return get_output("get-thermoregulator-settings")

def set_temp(temp):
    try:
        return set_input("set-thermoregulator-temp", [temp])[0].rstrip() == 'ok'
    except Exception:
        return False

#print(get_temp_settings())
#print(set_temp(20))
#print(get_temp_settings())