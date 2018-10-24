from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/')
def host_list(request):
    return render(request, 'host_list.html')
