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
    hosts = Host.objects.all()
    return render(request, 'host.html', {'data': hosts})


@login_required(login_url='/')
def host_input(request):
    '''
    当需要增加或修改主机信息时,需要进入输入页面填写信息.
    这个函数返回信息输入页面
    :param request:
    :return:
    '''
    response = {}
    if request.method == 'POST':
        response['ip'] = request.POST.get('ip')
        response['hostname'] = request.POST.get('hostname')
        response['group'] = request.POST.get('group')
    return render(request, 'host_input.html', response)


@login_required(login_url='/')
def host_apis(request):
    if request.method != 'POST':
        return redirect('host')

    action = request.POST.get('action')
    if action == 'insert':
        ip = request.POST.get('ip')
        hostname = request.POST.get('hostname')
        group = request.POST.get('group')
        host = Host(ip=ip, hostname=hostname, group=Group.objects.get(group=group))
        host.save(force_insert=True)
    elif action == 'delete':
        ip = request.POST.get('ip')
        host = Host.objects.filter(ip=ip).first()
        host.delete()

    return redirect('host_list')
