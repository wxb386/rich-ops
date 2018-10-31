from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .models import Address, Host, Param, Task
from ssh_client import login, ssh, sftp


def task_list(request):
    params = Param.objects.all()
    tasks = Task.objects.all()
    out = {}
    out['params'] = params
    out['tasks'] = tasks
    out['button'] = [
        {'url': '/cmdb/input/', 'method': 'update', 'submit': '修改'},
        {'url': '/cmdb/apis/', 'method': 'delete', 'submit': '删除'},
    ]
    return render(request, 'task_list.html', context=out)


def param_apis(request, method, pk):
    path = request.POST.get('path')
    format = request.POST.get('format')
    content = request.POST.get('content')
    if method == 'insert':
        Param(name=pk, path=path,
              format=format, content=content,
              created='2000-01-01', updated='2000-01-01').save()
    elif method == 'update':
        param = Param.objects.get(name=pk)
        param.path = path
        param.content = content
        param.save()
    elif method == 'delete':
        Param.objects.get(name=pk).delete()
    return redirect(task_list)


def task_apis(request, method, pk):
    path = request.POST.get('path')
    format = request.POST.get('format')
    content = request.POST.get('content')
    if method == 'insert':
        Task(name=pk, path=path,
             format=format, content=content,
             created='2000-01-01', updated='2000-01-01').save()
    elif method == 'update':
        task = Task.objects.get(name=pk)
        task.path = path
        task.content = content
        task.save()
    elif method == 'delete':
        Task.objects.get(name=pk).delete()
    return redirect(task_list)
