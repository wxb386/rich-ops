from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout


# Create your views here.
def index(request):
    return render(request, 'index.html')


def do_login(request):
    if request.method != 'POST':
        return redirect('index')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('host')
    return render(request, 'index.html', {'username': username, 'password': password, })


def do_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/')
def home(request):
    return render(request, 'home.html', {'username': request.user.username})
