import subprocess
import time
import os, re
from paramiko import SSHClient
from scp import SCPClient

GET = 'scm_scripts/get_values.scm'
SET = 'scm_scripts/set_values.scm'
USER = 'root'
FOLDER = '/root/control/'
SERVER = '192.168.17.13'

def get_output():
    '''
    Reads output from bioreactor by calling a Scheme script
    '''
    ssh = SSHClient() 
    ssh.load_system_host_keys()
    ssh.connect(SERVER, username=USER)

    sftp = ssh.open_sftp()
    sftp.put(GET, FOLDER + os.path.basename(GET))

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("gosh " + FOLDER + re.escape(os.path.basename(GET)))

    print(ssh_stderr.readlines())
    
    sftp.close()
    ssh.close()

    return #eval(result.stdout.decode('utf-8'))


def set_input(value, input):
    '''
    Sets particular <input> for bioreactor to <value> 
    Requires definition of possible inputs.
    '''
    ssh = SSHClient() 
    ssh.load_system_host_keys()
    ssh.connect(SERVER, username=USER)

    sftp = ssh.open_sftp()
    sftp.put(SET, FOLDER + os.path.basename(SET))

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("gosh " + FOLDER + re.escape(os.path.basename(SET)) \
                                        + " " + str(value) + " " + input)

    print("gosh " + FOLDER + re.escape(os.path.basename(SET)) \
                                        + " " + str(value) + " " + input)

    print(ssh_stdout.readlines())

    sftp.close()
    ssh.close()

# while True:
#     print(get_output())
#     time.sleep(2)

print(get_output())
set_input(10, "set-valve-tflow")