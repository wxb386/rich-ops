from django.shortcuts import render, redirect, HttpResponse
from django.forms.models import model_to_dict
from .models import Address, Host, Task
from .apis import cmdb_apis

from time import sleep


# Create your views here.


def cmdb_input(request):
    if request.method != 'POST':
        return render(request, 'cmdb_error.html')

    database = request.POST.get('_database')
    method = request.POST.get('_method')
    pk = request.POST.get('_pk')

    out = {database: True, 'database': database, 'method': method}
    # if pk == None:
    #     return render(request, 'cmdb_input.html', out)

    if database == 'address':
        if method == 'update':
            address = Address.objects.get(ip=pk)
            out['input'] = model_to_dict(address)
    elif database == 'host':
        if method == 'update':
            host = Host.objects.get(hostname=pk)
            out['input'] = model_to_dict(host)
        out['value'] = Address.objects.all()
    elif database == 'task':
        if method == 'update':
            task = Task.objects.get(name=pk)
            out['input'] = model_to_dict(task)
    return render(request, 'cmdb_input.html', out)


def host_list(request):
    addresses = Address.objects.all()
    hosts = Host.objects.all()
    out = {}
    out['addresses'] = addresses
    out['hosts'] = hosts
    out['button'] = [
        {'url': '/cmdb/input/', 'method': 'update', 'submit': '修+改'},
        {'url': '/cmdb/apis/', 'method': 'delete', 'submit': '删+除'},
    ]
    res = render(request, 'host_list.html', context=out)
    return res


def host_apis(request, method, pk):
    ip = request.POST.getlist('ip')
    print('ip==', ip)
    group = request.POST.get('group')
    cpu_core = request.POST.get('cpu_core')
    memory_total = request.POST.get('memory_total')
    nic_list = request.POST.get('nic_list')
    disk_list = request.POST.get('disk_list')
    if method == 'insert' or method == 'update':
        Host(
            hostname=pk,
            ip=ip, group=group,
            cpu_core=cpu_core, memory_total=memory_total,
            nic_list=nic_list, disk_list=disk_list
        ).save()
    elif method == 'delete':
        host = Host.objects.get(hostname=pk)
        host.delete()
    return redirect(host_list)


def host_info(request):
    return render(request, 'index.html')


def task_list(request):
    tasks = Task.objects.all()
    out = {}
    out['tasks'] = tasks
    out['button'] = [
        {'url': '/cmdb/input/', 'method': 'update', 'submit': '修改'},
        {'url': '/cmdb/apis/', 'method': 'delete', 'submit': '删除'},
    ]
    return render(request, 'task_list.html', context=out)


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


def execute_apis(request, method):
    return HttpResponse(request.POST)


def task_choose(request):
    address = Address.objects.all()
    tasks = Task.objects.all()
    out = {
        'all_ip': address,
        'all_task': tasks,
    }
    return render(request, 'execute_01.html', out)


def cmdb_server(request):
    import server_res
    server_stat = server_res.start()
    return render(request, 'server_stat.html', server_stat)
