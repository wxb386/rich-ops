from django.db import models

# Create your models here.

print('加载cmdb/models.py')


class Address(models.Model):
    ip = models.GenericIPAddressField('ip地址', primary_key=True)
    route = models.GenericIPAddressField('路由地址', null=False)
    port = models.IntegerField('跳转端口', null=False)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return '%s' % (self.ip,)


#
class Host(models.Model):
    '''
    主键是主机名,一台主机有多个ip地址
    '''
    hostname = models.CharField('主机名', max_length=64, primary_key=True)
    ip = models.ManyToManyField(Address, 'ip地址')
    group = models.CharField('群组', max_length=16, null=False)
    cpu_core = models.IntegerField('CPU', default=0)
    memory_total = models.IntegerField('内存', default=0)
    nic_list = models.TextField('网络接口', default='')
    disk_list = models.TextField('磁盘', default='')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return '%s:%s' % (self.hostname, self.group,)


class Task(models.Model):
    name = models.CharField('任务名称', max_length=32, primary_key=True)  # 这个任务的名称,任务通过名称进行关联
    path = models.CharField('目标路径', max_length=128, null=False)  # 将要传送到远程机器时,保存的路径
    param = models.CharField('获取参数路径', max_length=128, null=False)
    lang = models.CharField('编写语言', max_length=8, null=False)
    content = models.TextField('正文内容', null=False)  # 内容
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return '%s -> %s' % (self.name, self.path,)
