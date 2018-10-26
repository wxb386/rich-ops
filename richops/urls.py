"""richops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
import host.views
import task.views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.do_login, name='login'),
    url(r'^logout$', views.do_logout, name='logout'),
    url(r'^home$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    # cmdb
    url(r'^group/input/$', host.views.group_input, name='group_input'),
    url(r'^group/apis/$', host.views.group_apis, name='group_apis'),
    url(r'^host/input/$', host.views.host_input, name='host_input'),
    url(r'^host/apis/$', host.views.host_apis, name='host_apis'),
    url(r'^host/', host.views.host_list, name='host_list'),
    # task
    url(r'^task/input/(?P<func>\w+)/$', task.views.task_input, name='task_input'),
    url(r'^param/apis/$', task.views.param_apis, name='param_apis'),
    # url(r'^task/input/$', task.views.task_input, name='task_input'),
    url(r'^task/apis/$', task.views.task_apis, name='task_apis'),
    # url(r'^format/input/$', task.views.format_input, name='format_input'),
    url(r'^format/apis/$', task.views.format_apis, name='format_apis'),
    url(r'^task/', task.views.task_list, name='task_list'),
]
