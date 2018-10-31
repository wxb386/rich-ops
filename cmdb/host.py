from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .models import Address, Host, Param, Task
from ssh_client import login, ssh, sftp


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
    return render(request, 'host_list.html', context=out)


def address_apis(request, method, pk):
    route = request.POST.get('route')
    port = request.POST.get('port')
    if method == 'insert' or method == 'update':
        Address(ip=pk, route=route, port=port).save()
    elif method == 'delete':
        address = Address.objects.get(ip=pk)
        address.delete()
    return redirect(host_list)


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
