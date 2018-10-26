from django.shortcuts import render
from .models import Format, Param, Task
from django.forms.models import model_to_dict


# Create your views here.

def task_input(request, func):
    out = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        query = None
        if func == 'format':
            query = Format.objects.filter(name=name).first()
        elif func == 'param':
            query = Param.objects.filter(name__exact=name).first()
        elif func == 'task':
            query = Task.objects.filter(name__exact=name).first()
        out = model_to_dict(query)
    return render(request, '%s_input.html' % func, out)


def format_apis(request):
    return


def param_apis(request):
    return


def task_apis(request):
    return


def task_list(request):
    formats = Format.objects.all()
    params = Param.objects.all()
    tasks = Task.objects.all()
    out = {
        'format_buttons': [
            {'url': '/task/input/format/', 'action': 'insert', 'value': '修改'},
            {'url': '/format/apis/', 'action': 'delete', 'value': '删除'},
        ],
        'param_buttons': [
            {'url': '/task/input/param', 'action': 'insert', 'value': '修改'},
            {'url': '/param/apis/', 'action': 'delete', 'value': '删除'},
        ],
        'task_buttons': [
            {'url': '/task/input/task', 'action': 'insert', 'value': '修改'},
            {'url': '/task/apis/', 'action': 'delete', 'value': '删除'},
        ],
        'formats': formats,
        'params': params,
        'tasks': tasks,
    }
    return render(request, 'task.html', out)
