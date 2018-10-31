from django.shortcuts import render, redirect, HttpResponse
from django.forms.models import model_to_dict
from .models import Address, Host, Param, Task
from .host import *
from .task import *

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
    elif database == 'param':
        if method == 'update':
            param = Param.objects.get(name=pk)
            out['input'] = model_to_dict(param)
    elif database == 'task':
        if method == 'update':
            task = Task.objects.get(name=pk)
            out['input'] = model_to_dict(task)
    return render(request, 'cmdb_input.html', out)


def cmdb_apis(request):
    if request.method != 'POST':
        return render(request, 'index.html')
    database = request.POST.get('_database')
    method = request.POST.get('_method')
    pk = request.POST.get('_pk')

    if database == 'address':
        return address_apis(request, method, pk)
    elif database == 'host':
        return host_apis(request, method, pk)
    elif database == 'param':
        return param_apis(request, method, pk)
    elif database == 'task':
        return task_apis(request, method, pk)

    return HttpResponse('cmdb_apis')
