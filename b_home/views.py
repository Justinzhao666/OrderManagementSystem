# -*- coding: utf-8 -*-
import datetime
import hashlib

import os
from PIL import Image, ImageFile
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from OrderManagementSystem import settings
from b_login.views import blogin_check
from c_index.models import Orders, Goods, GoodCategory, C_UserInfo



### 用户篇
# 管理所有的用户
@blogin_check
def admin_user_all(request):
    users = C_UserInfo.objects.all()
    dicts = {'users': users, 'count': len(users)}
    return render(request, 'back/user/index.html', dicts)


# 针对单个用户编辑
@blogin_check
def admin_user_edit(request):
    uid = request.GET.get('uid')
    user = C_UserInfo.objects.get(user_account=uid)
    dicts = {'user': user}
    return render(request, 'back/user/edit.html', dicts)


# 保存用户
@blogin_check
def admin_user_save(request):
    data_post = request.POST
    username = data_post.get('username', None)
    if username == '':
        return HttpResponse('用户账户不可以为空')
    pwd = data_post.get('pwd', None)
    realname1 = data_post.get('realname1', None)
    realname2 = data_post.get('realname2', None)
    gender = data_post.get('gender', None)
    telecom = data_post.get('telecom', None)
    phone = data_post.get('phone', None)
    company = data_post.get('company', None)
    address = data_post.get('address', None)
    delete = data_post.get('delete', None)
    # 查询用户
    user = C_UserInfo.objects.filter(user_account=username)
    print('***************')
    print(username)
    print(gender)
    print(user)
    if user:
        user = user[0]
        if pwd:  # 修改密码，没有值就为原来的密码
            user.user_pwd = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
        else:
            pass
    else:
        user = C_UserInfo()
        user.user_account = username
        if pwd:
            user.user_pwd = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
        else:
            return HttpResponse('必须输入密码')
    user.user_firstname = realname1
    user.user_secondname = realname2
    user.user_gender = gender
    user.user_telecom = telecom
    user.user_phone = phone
    user.user_company = company
    user.user_addr = address
    if delete == 'True':
        user.isdelete = True
    else:
        user.isdelete = False
    user.save()
    return redirect('/admin_user_edit/?uid=' + username)


# 添加单个用户
@blogin_check
def admin_user_add(request):
    return render(request, 'back/user/add.html')

@blogin_check
def user_check(request):
    data_uid = request.GET.get('uid', None)
    if C_UserInfo.objects.filter(user_account=data_uid):
        return HttpResponse('0')
    else:
        return HttpResponse('1')


### 订单篇
# 管理所有的订单 分4个逻辑 0-3
@blogin_check
def admin_order(request, cate):
    order_list = ''
    if cate == '0':  # 未发货订单
        order_list = Orders.objects.filter(state='待发货', isdelete=False).order_by('-time_begin')
    if cate == '1':  # 发货未送达订单
        order_list = Orders.objects.filter(state='发货中', isdelete=False)
    if cate == '2':  # 未付款订单
        order_list = Orders.objects.filter(state='收货未付款', isdelete=False)
    if cate == '3':  # 完成的订单
        order_list = Orders.objects.filter(state='完成', isdelete=False)
    if cate == '4':  # 所有订单
        order_list = Orders.objects.filter(isdelete=False)
    if cate == '5':  # 被取消的订单
        order_list = Orders.objects.filter(isdelete=True)
    for order in order_list:
        goods = order.orderinfo_set.all()
    dict = {'orders': order_list, 'count': len(order_list)}
    print(dict)
    return render(request, 'back/order/index.html', dict)


# 显示订单详情
@blogin_check
def admin_showorder(request):
    getdata = request.GET
    oid = getdata.get('oid')
    order = Orders.objects.get(oid=oid)
    goods = order.orderinfo_set.all()
    dicts = {'order': order, 'goods': goods}
    return render(request, 'back/order/info.html', dicts)


# 订单报表 ---和上面一个函数！
@blogin_check
def admin_reportorder(request):
    getdata = request.GET
    oid = getdata.get('oid')
    order = Orders.objects.get(oid=oid)
    goods = order.orderinfo_set.all()
    dicts = {'order': order, 'goods': goods}
    return render(request, 'back/order/report.html', dicts)


## 大量的重复代码需要去优化-- 换个思路 这里之前有一个很蠢的思路，针对每一个点击都给他一个view方法，愚蠢透顶！
@blogin_check
def admin_change_order_state(request):
    data_oid = request.GET.get('oid', None)
    data_page = request.GET.get('page', None)
    data_state = request.GET.get('state', None)
    order = Orders.objects.get(oid=data_oid)
    if order.isdelete:
        return HttpResponse('该订单已经被用户取消了')
    if data_state == '完成':
        order.time_end = datetime.datetime.now()
        goods = order.orderinfo_set.all()
        for good in goods:  # 设置销量,这地方是有缺陷的：完成状态取消的话，销量应该还原回去！先不做！
            good.gid.count_sell = good.gid.count_sell + good.count
            good.gid.save()
    else:
        order.time_end = None
    order.state = data_state
    order.save()
    return redirect('/admin_order/' + data_page + '/')


### 商品篇
# 管理所有的商品
@blogin_check
def admin_good_all(request):
    goods = Goods.objects.all()
    dict = {'goods': goods, 'count': len(goods)}
    return render(request, 'back/good/index.html', dict)


# 查看和编辑单个商品
@blogin_check
def admin_good_info(request):
    data_gid = request.GET.get('gid', None)
    good = Goods.objects.get(gid=data_gid)
    cates = GoodCategory.objects.all()
    dict = {'good': good, 'cates': cates}
    return render(request, 'back/good/info.html', dict)


# 添加单个商品
@blogin_check
def admin_good_add(request):
    cates = GoodCategory.objects.all()
    dicts = {'cates': cates}
    return render(request, 'back/good/add.html', dicts)

@blogin_check
def gid_check(request):
    data_gid = request.GET.get('gid', None)
    if Goods.objects.filter(gid=data_gid):
        return HttpResponse('0')
    else:
        return HttpResponse('1')


# 保存修改和添加
@blogin_check
def admin_good_save(request):
    data_post = request.POST
    goodid = data_post.get('gid', None)
    if goodid == '':
        return HttpResponse('订单编号不能为空')
    goods = Goods.objects.filter(gid=goodid)  # 这里就获取到商品
    if goods:
        good = goods[0]
    else:
        good = Goods()
    good.gid = goodid
    name = data_post.get('name', None)
    cate = data_post.get('cate', None)
    count = data_post.get('count', None)
    unit = data_post.get('unit', None)
    price1 = data_post.get('price1', None)
    price2 = data_post.get('price2', None)
    shortinfo = data_post.get('shortinfo', None)
    info = data_post.get('info', None)
    # 保存图片
    if 'photo' in request.FILES:  # 区别不传文件情况下
        pic = request.FILES['photo']
        img = Image.open(pic)
        pic_tmpname = goodid + '.' + str(pic.name).split('.')[-1]
        fname = '%sgoods/%s' % (settings.MEDIA_ROOT, pic_tmpname)
        img.save(fname)
        good.good_pic = r'goods/' + pic_tmpname
    else:
        pass
    # end 保存图片
    delete = data_post.get('delete', None)
    good.good_name = name
    good.cate_id = GoodCategory.objects.get(id=int(cate))
    good.count = count
    good.unit = unit
    good.price_sell = price1
    good.price_orgin = price2
    good.good_shortinfo = shortinfo
    good.good_info = info
    if delete == 'True':
        good.isdelete = True
    else:
        good.isdelete = False
    good.save()
    return redirect('/admin_good_info/?gid=' + str(goodid))

# 计算收益
@blogin_check
def admin_profit(request):
    orders = Orders.objects.filter(isdelete=False,state='完成').order_by('-time_end')
    dicts = {'orders':orders}
    return render(request,'back/profit/index.html',dicts)
