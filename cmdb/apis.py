from django.shortcuts import render
from . import address, tasks


# apis仅处理数据库操作
# apis应返回json格式的http页面数据
# 里面调用的每个apis函数应返回json数据字符串
def cmdb_apis(request):
    if request.method != 'POST':
        return render(request, 'index.html')
    database = request.POST.get('_database')
    method = request.POST.get('_method')
    pk = request.POST.get('_pk')
    out = None
    if database == 'address':
        out = address.apis(request, method, pk)
    elif database == 'host':
        return host_apis(request, method, pk)
    elif database == 'task':
        return task_apis(request, method, pk)
    elif database == 'execute':
        return execute_apis(request, method)

    return HttpResponse('cmdb_apis')
