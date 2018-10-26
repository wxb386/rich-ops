from django.db import models


# Create your models here.

class Group(models.Model):
    group = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.group


class Host(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    hostname = models.CharField(max_length=50, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s -> %s' % (self.ip, self.hostname, self.group)
