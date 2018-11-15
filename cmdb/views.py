from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Address, Host, Script, Task, Job


# Create your views here.

class IndexView(TemplateView):
    template_name = 'cmdb/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['all_jobs'] = Job.objects.all()
        return context


def run(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if job.status == '已创建':
        job.status = '已完成'
        job.save()
    return redirect('cmdb:index')
