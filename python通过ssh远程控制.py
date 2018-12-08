import paramiko
# import email
def ssh(sys_ip,username,password,cmds):
    try:
        #创建ssh客户端
        client = paramiko.SSHClient()
        #第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #密码方式远程连接
        client.connect(sys_ip, 22, username=username, password=password, timeout=20)
        #互信方式远程连接
        #key_file = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
        #ssh.connect(sys_ip, 22, username=username, pkey=key_file, timeout=20)
        #执行命令
        stdin, stdout, stderr = client.exec_command(cmds)
        #获取命令执行结果,返回的数据是一个list
        result = stdout.readlines()
        return result
    except:
        print("error!")
    finally:
        client.close()
 
if __name__=="__main__":
    sys_ip = "172.31.103.189"
    username = "pi"
    password = "66778899"
    cmds = "ls"
    print(ssh(sys_ip,username,password,cmds))
    cmd = "df -hl"    #check the store
    results = ssh(sys_ip,username,password,cmd)
    for line in results:
        print(line)