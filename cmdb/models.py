from django.db import models


# Create your models here.


#
class Host(models.Model):
    hostname = models.CharField('主机名', max_length=64, primary_key=True)
    group = models.CharField('群组', max_length=16, default='WebServer')
    other = models.TextField('其他', default='{}')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return '%s:%s' % (self.hostname, self.group)


class Address(models.Model):
    ip = models.GenericIPAddressField('ip地址', primary_key=True)
    route = models.GenericIPAddressField('路由地址', null=False)
    port = models.IntegerField('跳转端口', null=False)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    host = models.ForeignKey(Host, verbose_name='主机', on_delete=models.CASCADE)

    def __str__(self):
        return '%s<-%s' % (self.ip, self.host)


class Script(models.Model):
    name = models.CharField('脚本名称', max_length=64, primary_key=True)  # 这个任务的名称,任务通过名称进行关联
    lang = models.CharField('编写语言', max_length=8, null=False)
    content = models.TextField('脚本内容', null=False)  # 内容
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return '%s:%s' % (self.name, self.lang)


class Task(models.Model):
    name = models.CharField('任务名称', max_length=64, primary_key=True)
    lang = models.CharField('编写语言', max_length=8, null=False)
    param = models.TextField('任务参数', null=False, default='')  # 内容
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    task = models.ForeignKey(Script, verbose_name='脚本', on_delete=models.CASCADE)

    def __str__(self):
        return '%s<-%s' % (self.name, self.task)


class Job(models.Model):
    task_name = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='任务')
    host_ip = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='主机地址')
    status = models.CharField('状态', max_length=32, null=False, default='已创建')
    other = models.TextField('其他', default='')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return '%s+%s' % (self.task_name, self.host_ip)
