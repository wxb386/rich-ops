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
import cmdb.views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.do_login, name='login'),
    url(r'^logout$', views.do_logout, name='logout'),
    url(r'^home$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    # cmdb
    url(r'^host/$', cmdb.views.host_list, name='host_list'),
    url(r'^task/$', cmdb.views.task_list, name='task_list'),
    url(r'^cmdb/input/$', cmdb.views.cmdb_input, name='cmdb_input'),
    url(r'^cmdb/apis/$', cmdb.views.cmdb_apis, name='cmdb_apis'),

]
