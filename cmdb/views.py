from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Job
from .tasks import remote_execute
from time import sleep



# Create your views here.

class IndexView(TemplateView):
    template_name = 'cmdb/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['all_jobs'] = Job.objects.all()
        return context


def run(request, job_id):
    print('sendto:%s' % job_id)
    remote_execute.delay(job_id)
    return redirect('cmdb:index')
