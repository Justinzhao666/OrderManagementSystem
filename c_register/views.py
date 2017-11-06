# -*- coding: utf-8 -*-
import hashlib

import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from c_index.models import C_UserInfo


def register(request):
    return render(request,'front/register.html',{'title':'佳驰'})

def register_handle(request):
    if request.method == 'GET':
        return render(request, 'front/register.html')
    elif request.method == 'POST':
        post = request.POST
        username = post.get('user_name')
        pwd = post.get('pwd')
        cpwd = post.get('cpwd')
        phone = post.get('phone')
        if username and len(pwd) >= 5 and phone and pwd ==cpwd:
            # 再次检验是否存在用户
            try:
                C_UserInfo.objects.get(user_account=username)
                return render(request, 'front/register.html')
            except:
                user = C_UserInfo()
                user.user_account = username
                user.user_pwd = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
                user.user_phone = phone
                user.user_lastlogin = datetime.datetime.now()
                user.save()
                print('->注册用户: '+username)
                # register完应该进入用户中心填写地址信息，并设置session
                ret = HttpResponseRedirect('/user_center_info/')
                request.session['username'] = user.user_account
                return ret
        else:
            return render(request, 'front/register.html')

def usercheck(request):
    username = request.GET.get('username', None)
    if username:
        try:
            if C_UserInfo.objects.get(user_account=username):
                pass
        except:
            print('exception:注册用户不存在可以注册')
            return JsonResponse({'exist': 'False'})
        else:
            print('user has exist:不允许注册')
            return JsonResponse({'exist': 'True'})
        finally:
            pass
    else:
        return HttpResponse('未接受到数据')