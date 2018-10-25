from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group, Host


# Create your views here.

@login_required(login_url='/')
def host_list(request):
    '''
    返回主机列表页面
    :param request:
    :return:
    '''
    groups = Group.objects.all()
    hosts = Host.objects.all()
    return render(request, 'host.html', {'hosts': hosts, 'groups': groups})


@login_required(login_url='/')
def host_input(request):
    '''
    当需要增加或修改主机信息时,需要进入输入页面填写信息.
    这个函数返回信息输入页面
    :param request:
    :return:
    '''
    groups = Group.objects.all()
    host = {}
    if request.method == 'POST':
        host['ip'] = request.POST.get('ip')
        host['hostname'] = request.POST.get('hostname')
        host['group'] = request.POST.get('group')
    return render(request, 'host_input.html', {'host': host, 'group': groups})


@login_required(login_url='/')
def host_apis(request):
    if request.method != 'POST':
        return redirect('host_list')

    action = request.POST.get('action')
    if action == 'insert':
        ip = request.POST.get('ip')
        hostname = request.POST.get('hostname')
        group = request.POST.get('group')
        host = Host(ip=ip, hostname=hostname, group=Group.objects.get(group=group))
        host.save()
    if action == 'update':
        ip = request.POST.get('ip')
        hostname = request.POST.get('hostname')
        group = request.POST.get('group')
        host = Host(ip=ip, hostname=hostname, group=Group.objects.get(group=group))
        host.update()
    elif action == 'delete':
        ip = request.POST.get('ip')
        host = Host.objects.filter(ip=ip).first()
        host.delete()

    return redirect('host_list')


@login_required(login_url='/')
def group_input(request):
    group = ''
    if request.method == 'POST':
        group = request.POST.get('group')
    return render(request, 'group_input.html', {'group': group})


@login_required(login_url='/')
def group_apis(request):
    if request.method != 'POST':
        return redirect('host_list')

    action = request.POST.get('action')
    group = request.POST.get('group')
    if action == 'insert':
        row = Group(group=request.POST.get('group'))
        row.save()
    elif action == 'delete':
        row = Group.objects.filter(group=group).first()
        row.delete()

    return redirect('host_list')
