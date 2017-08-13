from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# def admin_check()

def blogin(request):
    return render(request,'back/blogin.html');
