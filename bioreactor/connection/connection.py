from paramiko import SSHClient
from scp import SCPClient

class SSHconnection():
    def __init__(self, server, user):
        self.ssh = SSHClient() 
        self.ssh.load_system_host_keys()
        self.ssh.connect(server, username=user)
        self.sftp = self.ssh.open_sftp()

    def put(self, file, location):
        self.sftp.put(file, location)

    def execute_cmd(self, command):
        return self.ssh.exec_command(command)

    def disconnect(self):
        self.__del__()

    def __del__(self):
        self.sftp.close()
        self.ssh.close()