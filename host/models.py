from django.db import models


# Create your models here.

class Group(models.Model):
    group = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.group


class Host(models.Model):
    ip = models.CharField(max_length=15, unique=True, null=False)
    hostname = models.CharField(max_length=50, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default='')

    def __str__(self):
        return '%s %s -> %s' % (self.ip, self.hostname, self.group)
