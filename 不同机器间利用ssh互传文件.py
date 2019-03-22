import paramiko
import uuid

class SSHConnection(object):

    def __init__(self, host='192.168.11.61', port=22, username='alex',pwd='alex3714'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def run(self):
        self.connect()
        pass
        self.close()

    def connect(self):
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        return result

    def upload(self,local_path, target_path):
        # 连接，上传
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path)

    def download(self,remote_file,local_file):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # sftp = ssh.open_sftp()
        sftp.get(remote_file, local_file)

ip = "139.199.185.239"
password = "66778899"
port = 22
user = 'ubuntu'

ssh = SSHConnection(ip,port,user,password)
ssh.connect()
r1 = ssh.cmd('df')
local_files = ["main.cpp",
         "src/CctpMdSpi.cpp",
        "src/CctpMdSpi.h"]

remote_file_pre = "/home/ubuntu/"
file_path = "projects/investment/code_by_hai/"
print("*"*60)
for local_file in local_files:
    remote_file = remote_file_pre+file_path+local_file
    ssh.upload(local_file,remote_file)
    # ssh.download(remote_file,local_file)
    print(local_file+" upload ok!")
print("*"*60)
print("upload over!")
result = ssh.cmd("ls "+remote_file_pre+file_path)
print(result.decode("utf-8").split("\n"))
ssh.close()
