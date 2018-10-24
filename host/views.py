from django.shortcuts import render

# Create your views here.
def host_list(request):
    return render(request,'host_list.html')