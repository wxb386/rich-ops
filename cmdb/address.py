from django.shortcuts import render
from .models import Address


def address_apis(request, method, pk):
    route = request.POST.get('route')
    port = request.POST.get('port')
    out = {}
    try:
        if method == 'insert' or method == 'update':
            Address(ip=pk, route=route, port=port).save()
        elif method == 'delete':
            address = Address.objects.get(ip=pk)
            address.delete()

        out['success'] = True
    except Exception as e:
        print(e)
        out['success'] = False
    return out
