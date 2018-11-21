from .models import Job
from celery import task, platforms
import paramiko
import os, logging

platforms.C_FORCE_ROOT = True


@task
def remote_execute(job_id):
    job = Job.objects.get(pk=job_id)
    keyfile = '/root/.ssh/id_rsa'
    user = 'root'
    temp_dir = '/dev/shm/'

    host = job.host_ip.route
    port = job.host_ip.port
    script = job.task_name.script.content.replace('\r', '')
    config = job.task_name.config.replace('\r', '')
    param = job.task_name.param.replace('\r', '')

    # 建立一个socket
    trans = paramiko.Transport((host, port))
    # 启动一个客户端
    trans.start_client()
    # 如果使用rsa密钥登录的话
    key = paramiko.RSAKey.from_private_key_file(keyfile)
    trans.auth_publickey(username=user, key=key)
    # 创建ssh
    ssh = paramiko.SSHClient()
    ssh._transport = trans
    # 创建scp
    scp = paramiko.SFTPClient.from_transport(trans)

    scr_filename = os.path.join(temp_dir, '_script')
    with open(scr_filename, 'wb+') as f:
        f.write(script.encode('utf-8'))

    conf_filename = os.path.join(temp_dir, '_config')
    with open(conf_filename, 'wb+') as f:
        f.write(config.encode('utf-8'))

    scp.put(scr_filename, scr_filename)
    scp.put(conf_filename, conf_filename)
    command = '/bin/bash %s %s' % (
        scr_filename,
        param,
    )
    print(command)

    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read()
    err = stderr.read()
    if len(err) > 0:
        logging.info(err)
        print('error:\n%s' % err.decode('utf-8'))
        return False
    logging.info(out)
    print('out:\n%s' % out.decode('utf-8'))
    return out
