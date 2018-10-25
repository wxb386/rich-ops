from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.host_list, name='host_list'),
    url(r'^input/$', views.host_input, name='host_input'),
    url(r'^apis/$', views.host_apis, name='host_apis'),
]
