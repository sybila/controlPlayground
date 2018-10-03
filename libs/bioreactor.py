import subprocess
import time
from paramiko import SSHClient
from scp import SCPClient

GET = ['gosh', 'scm_scripts/get_values.scm']
SET = ['gosh', 'scm_scripts/set_values.scm']
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

    sftp.put(file, FOLDER + os.path.basename(GET[1]))

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("gosh " + FOLDER + re.escape(os.path.basename(file)))

    print(ssh_stdin, ssh_stdout, ssh_stderr)
    
    sftp.close()
    ssh.close()

    return #eval(result.stdout.decode('utf-8'))


def set_input(value, input):
    '''
    Sets particular <input> for bioreactor to <value> 
    Requires definition of possible inputs.
    '''
    subprocess.call(SET + [str(value), input])


# while True:
#     print(get_output())
#     time.sleep(2)

print(get_output())
set_input(10, "set-valve-tflow")