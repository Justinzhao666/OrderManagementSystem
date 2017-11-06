# -*- coding: utf-8 -*-
import hashlib

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.

# def admin_check()
from c_index.models import B_Admin


def blogin(request):
    return render(request, 'back/blogin.html');


def blogin_handle(request):
    if request.method == 'GET':
        return render(request, 'front/login.html')
    aname = request.POST.get('username', None)
    apwd = request.POST.get('pwd', None)
    passkey = hashlib.md5('admin9527'.encode(encoding='utf-8')).hexdigest()
    print('passkey:' + passkey)
    if aname and apwd:
        if aname == 'admin9527' and hashlib.md5(apwd.encode(encoding='utf-8')).hexdigest() == passkey:
            request.session['admin'] = aname
            dict = {'admin': aname}
            return render(request, 'back/index.html/', dict)
        else:
            return HttpResponse('账号输入有误！')
    else:
        return HttpResponse('用户名密码不能为空')


def admin_logout(request):
    if request.session.get('admin', default=None):
        del request.session['admin']
    return redirect('/OMS_admin/blogin/')


# 检验是否登录
def blogin_check(fun):
    def login_fun(request, *args, **kwargs):
        if request.session.has_key('admin'):
            return fun(request, *args, **kwargs)
        else:
            ret = HttpResponseRedirect('/OMS_admin/blogin/')
        return ret
    return login_fun
