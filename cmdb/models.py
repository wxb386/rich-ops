from django.db import models


# Create your models here.


class Address(models.Model):
    ip = models.GenericIPAddressField(primary_key=True, verbose_name='ip地址')
    route = models.GenericIPAddressField(null=False, verbose_name='路由地址')
    port = models.IntegerField(null=False, verbose_name='跳转端口')

    def __str__(self):
        return '%s' % (self.ip,)


#
class Host(models.Model):
    '''
    主键是主机名,一台主机有多个ip地址
    '''
    group_choices = (
        ("WebServer", 0),
        ("DBServer", 1),
    )

    hostname = models.CharField(max_length=64, primary_key=True, verbose_name='主机名')
    ip = models.ManyToManyField(Address, verbose_name='ip地址')
    group = models.CharField(max_length=16, choices=group_choices, verbose_name='群组', null=False, default='WebServer')
    cpu_core = models.IntegerField(verbose_name='CPU', default=0)
    memory_total = models.IntegerField(verbose_name='内存', default=0)
    nic_list = models.TextField(verbose_name='网络接口', default='')
    disk_list = models.TextField(verbose_name='磁盘', default='')

    def __str__(self):
        return '%s:%s' % (self.hostname, self.group,)


class Param(models.Model):
    format_choices = (
        ('py2', '/usr/bin/python2.7'),
        ('py3', '/usr/bin/python3.6'),
        ('sh', '/bin/bash'),
        ('txt', '/usr/bin/cat'),
    )

    name = models.CharField(max_length=32, primary_key=True)  # 这个参数文件的名称,任务通过名称进行关联
    path = models.CharField(max_length=128, null=False)  # 将要传送到远程机器时,保存的路径
    format = models.CharField(max_length=8, choices=format_choices, null=False, default='txt', verbose_name='格式')
    content = models.TextField(null=False)  # 内容
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s -> %s' % (self.name, self.path)


class Task(models.Model):
    format_choices = (
        ('py2', '/usr/bin/python2.7'),
        ('py3', '/usr/bin/python3.6'),
        ('sh', '/bin/bash'),
        ('txt', '/usr/bin/cat'),
    )

    name = models.CharField(max_length=32, primary_key=True)  # 这个任务的名称,任务通过名称进行关联
    path = models.CharField(max_length=128, null=False)  # 将要传送到远程机器时,保存的路径
    format = models.CharField(max_length=8, choices=format_choices, null=False, default='txt', verbose_name='格式')
    content = models.TextField(null=False)  # 内容
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s -> %s' % (self.name, self.path)
