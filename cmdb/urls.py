from django.conf.urls import url
from . import views

app_name = 'cmdb'
urlpatterns = [
    url(r'^jobs/$', views.IndexView.as_view(), name='index'),
    url(r'^jobs/(?P<job_id>[0-9]+)/$', views.run, name='run'),
]
