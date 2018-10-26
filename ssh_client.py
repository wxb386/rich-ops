#!/usr/bin/python3
import paramiko
import os
import select
import sys
import tty
import termios
from settings import *

'''
实现一个xshell登录系统的效果，登录到系统就不断输入命令同时返回结果
支持自动补全，直接调用服务器终端

'''


def login():
    # 建立一个socket
    trans = paramiko.Transport((SSH_IP, SSH_PORT))
    # 启动一个客户端
    trans.start_client()

    try:
        # 如果使用rsa密钥登录的话
        key = paramiko.RSAKey.from_private_key_file(SSH_KEY_FILE)
        trans.auth_publickey(username=SSH_USERNAME, key=key)
    except Exception as e:
        # 如果使用用户名和密码登录
        trans.auth_password(username=SSH_USERNAME, password=SSH_PASSWORD)
    return trans


def ssh(trans):
    '''
    传入ssh-socket对象,返回ssh-client对象,可以执行命令和返回结果

    stdin, stdout, stderr = ssh-client.exec_command('df -hl')
    print(stdout.read().decode())

    最后,关闭trans

    trans.close()

    :param trans:
    :return:ssh-client
    '''
    # 将sshclient的对象的transport指定为以上的trans
    client = paramiko.SSHClient()
    client._transport = trans
    return client


def sftp(trans):
    '''
    传入ssh-socket对象,返回sftp-client对象,可以上传和下载文件

    sftp-client.put(本地源路径, 远程目标路径)
    sftp-client.get(远程源路径, 本地目标路径)

    最后,关闭trans

    trans.close()

    :param trans:
    :return:
    '''
    # 实例化一个 sftp对象,指定连接的通道
    client = paramiko.SFTPClient.from_transport(login())
    return client


def xshell():
    trans = login()
    # 打开一个通道
    channel = trans.open_session()
    # 获取终端
    channel.get_pty()
    # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
    channel.invoke_shell()
    # 获取原操作终端属性
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        # 将现在的操作终端属性设置为服务器上的原生终端属性,可以支持tab了
        tty.setraw(sys.stdin)
        channel.settimeout(0)

        while True:
            readlist, writelist, errlist = select.select([channel, sys.stdin, ], [], [])
            # 如果是用户输入命令了,sys.stdin发生变化
            if sys.stdin in readlist:
                # 获取输入的内容，输入一个字符发送1个字符
                input_cmd = sys.stdin.read(1)
                # 将命令发送给服务器
                channel.sendall(input_cmd)

            # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
            if channel in readlist:
                # 获取结果
                result = channel.recv(1024)
                # 断开连接后退出
                if len(result) == 0:
                    print("\r\n**** EOF **** \r\n")
                    break
                # 输出到屏幕
                sys.stdout.write(result.decode())
                sys.stdout.flush()
    finally:
        # 执行完后将现在的终端属性恢复为原操作终端属性
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        # 关闭通道
        channel.close()
    trans.close()


if __name__ == '__main__':
    xshell()
