# -*- coding: utf-8 -*-
import hashlib

from django.db.models.functions import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from c_index.models import C_UserInfo


def login(request):
    return render(request,'front/login.html',{'title':'佳驰'})

def login_handle(request):
    # 防恶意攻击
    if request.method == 'GET':
        return render(request, 'front/login.html')
    elif request.method == 'POST':
        post = request.POST
        uname = post.get('username',None) # None为取不到name的默认值
        upwd = post.get('pwd',None)
        rember = post.get('check',0) # html中值为1，这里如果记住就是1，如果没选择记住就为0
        if uname and upwd:
            # 如果填入不为空
            user = C_UserInfo.objects.filter(user_account=uname,isdelete=False)  # 如果使用get取不到就或抛出异常
            if len(user)==1:
                # 登录成功
                if hashlib.md5(upwd.encode(encoding='utf-8')).hexdigest() == user[0].user_pwd:
                    url = request.COOKIES.get('url','/') # 当用户在未登录情况下点击需要登录才可以显示的地方，登录完后跳转用户想要去的地方
                    ret = HttpResponseRedirect(url)
                    if rember != 0:
                        ret.set_cookie('username',uname)
                    else:
                        ret.set_cookie('username','',max_age=-1)
                    request.session['username'] = uname
                    # request.session['firstname'] = user[0].user_firstname
                    # 保留登录成功时间
                    user.update(user_lastlogin = datetime.datetime.now())
                    return ret
                else:
                    return render(request, 'front/login.html', {'error': {'password': '密码输入有误，请重新输入'}})
            else:
                return render(request, 'front/login.html', {'error': {'name': '用户名不存在，请重新输入'}})
        else:
            return render(request, 'front/login.html', {'error': {'name': '请输入用户名', 'password': '请输入密码'}})


