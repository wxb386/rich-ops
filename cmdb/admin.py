from django.contrib import admin
from .models import Address, Host, Param, Task

# Register your models here.


admin.site.register(Address)
admin.site.register(Host)
admin.site.register(Param)
admin.site.register(Task)
