#!/usr/bin/python3
import paramiko


class SSH_Client():
    _host = None
    _port = None
    _user = None
    _keyfile = None
    _trans = None
    _ssh = None
    _scp = None

    def __init__(self, host, port, user, keyfile):
        self._host = host
        self._port = port
        self._user = user
        self._keyfile = keyfile
        self._trans = self.login(host, port, user, keyfile)

    def login(self, host, port, user, keyfile):
        # 建立一个socket
        trans = paramiko.Transport((host, port))
        # 启动一个客户端
        trans.start_client()

        try:
            # 如果使用rsa密钥登录的话
            key = paramiko.RSAKey.from_private_key_file(keyfile)
            trans.auth_publickey(username=user, key=key)
        except Exception as e:
            print(e)
            return None
        return trans

    def run(self, command):
        # 将sshclient的对象的transport指定为以上的trans
        if self._ssh == None:
            self._ssh = paramiko.SSHClient()
        self._ssh._transport = self._trans
        stdin, stdout, stderr = self._ssh.exec_command(command)
        out = stdout.read()
        err = stderr.read()
        if len(err) > 0:
            print(err.decode())
        return out

    def put(self, localfile, remotefile):
        # 实例化一个 sftp对象,指定连接的通道
        if self._scp == None:
            self._scp = paramiko.SFTPClient.from_transport(self._trans)
        self._scp.put(localfile, remotefile)

    def get(self, remotefile, localfile):
        # 实例化一个 sftp对象,指定连接的通道
        if self._scp == None:
            self._scp = paramiko.SFTPClient.from_transport(self._trans)
        self._scp.get(remotefile, localfile)
