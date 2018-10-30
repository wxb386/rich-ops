from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .models import Address, Host, Param, Task


# Create your views here.

def host_list(request):
    addresses = Address.objects.all()
    hosts = Host.objects.all()
    out = {}
    out['addresses'] = addresses
    out['hosts'] = hosts
    out['button'] = [
        {'url': '/cmdb/input/', 'method': 'update', 'submit': '修改'},
        {'url': '/cmdb/apis/', 'method': 'delete', 'submit': '删除'},
    ]
    return render(request, 'host_list.html', context=out)


def task_list(request):
    params = Param.objects.all()
    tasks = Task.objects.all()
    out = {}
    out['params'] = model_to_dict(params)
    out['tasks'] = model_to_dict(tasks)
    return render(request, 'task_list.html', context=out)


# url(r'^host/$', cmdb.views.host_list, name='host_list'),
# url(r'^task/$', cmdb.views.task_list, name='task_list'),
# url(r'^cmdb/input/(?P<database>[0-9a-zA-Z]+)/(?P<action>\w+)/$',
#     cmdb.views.cmdb_input, name='cmdb_input'),
# url(r'^cmdb/apis/$', cmdb.views.cmdb_apis, name='cmdb_apis'),
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
        if method == 'insert':
            host = {}
            host['ip'] = Address.objects.all()
            out['host'] = host
            print(out)
        elif method == 'update':
            host = Host.objects.get(ip=pk)
            out['input'] = model_to_dict(host)
    return render(request, 'cmdb_input.html', out)


def cmdb_apis(request):
    if request.method != 'POST':
        return render(request, 'index.html')
    database = request.POST.get('_database')
    method = request.POST.get('_method')
    pk = request.POST.get('_pk')

    if database == 'address':
        route = request.POST.get('route')
        port = request.POST.get('port')
        if method == 'insert':
            Address(ip=pk, route=route, port=port).save()
        elif method == 'update':
            address = Address.objects.get(ip=pk)
            address.route = route
            address.port = port
            address.save()
        elif method == 'delete':
            address = Address.objects.get(ip=pk)
            address.delete()
        return redirect(host_list)

    elif database == 'host':

        pass

    return redirect(host_list)
