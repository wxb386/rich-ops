from django.shortcuts import render, redirect
from django.forms.models import model_to_dict


def jobs_list(request):
    return render(request, 'jobs_list.html')


def jobs_input(request):
    return render(request, 'jobs_list.html')


def jobs_apis(request):
    return redirect(jobs_list)


