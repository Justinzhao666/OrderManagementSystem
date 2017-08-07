from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def homepage():
    return HttpResponse('管理员界面')