from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def blogin(request):
    # return render(request,)
    return HttpResponse('这是管理员登录的页面')