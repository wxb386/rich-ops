from django.contrib import admin
from .models import Format, Param, Task

# Register your models here.

admin.site.register(Format)
admin.site.register(Param)
admin.site.register(Task)
