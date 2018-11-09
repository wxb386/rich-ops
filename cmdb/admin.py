from django.contrib import admin
from .models import Address, Host, Script, Task, Job

# Register your models here.


admin.site.register(Address)
admin.site.register(Host)
admin.site.register(Script)
admin.site.register(Task)
admin.site.register(Job)
