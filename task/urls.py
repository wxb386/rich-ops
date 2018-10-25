from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.host_list,name='host_list'),
]