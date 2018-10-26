from django.db import models


# Create your models here.
class Format(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    command = models.CharField(max_length=64, null=False)

    def __str__(self):
        return '%s:%s' % (self.name, self.command)


class Param(models.Model):
    name = models.CharField(max_length=32, primary_key=True)  # 这个参数文件的名称,任务通过名称进行关联
    path = models.CharField(max_length=127, null=False)  # 将要传送到远程机器时,保存的路径
    format = models.ForeignKey(Format, on_delete=models.CASCADE)  # 格式,一般是py或sh
    content = models.TextField(null=False)  # 内容
    created = models.DateTimeField(auto_created=True, null=False)
    updated = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return '参数文件[%s]: %s -> %s ' % (self.format, self.name, self.path)


class Task(models.Model):
    name = models.CharField(max_length=32, primary_key=True)  # 这个任务的名称,任务通过名称进行关联
    path = models.CharField(max_length=127, null=False)  # 将要传送到远程机器时,保存的路径
    format = models.ForeignKey(Format, on_delete=models.CASCADE)  # 格式,一般是py或sh
    content = models.TextField(null=False)  # 内容
    created = models.DateTimeField(auto_created=True, null=False)
    updated = models.DateTimeField(auto_now_add=True, null=False)
