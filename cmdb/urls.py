from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^host/$', views.host_list, name='host_list'),
    url(r'^task/$', views.task_list, name='task_list'),
    url(r'^input/$', views.cmdb_input, name='cmdb_input'),
    url(r'^apis/$', views.cmdb_apis, name='cmdb_apis'),
    url(r'^server/$', views.cmdb_server, name='cmdb_server'),
    url(r'^task_choose/$', views.task_choose, name='task_choose'),
]
