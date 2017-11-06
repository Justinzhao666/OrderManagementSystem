# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from c_index import user_decorator

# 获取自己的购物车
from c_index.models import *


@user_decorator.login_check
@user_decorator.check_session
def cart(request,dict_user):
    cartlist = dict_user['user'].cart_set.all()
    cart_good_list = []
    for cart in cartlist:
        cart_good_list.append({'cart': cart, 'good': Goods.objects.get(gid=cart.gid_id)})
    # print('cart_list:'+str(cart_good_list))
    dic = dict(dict_user, **{'list': cart_good_list})
    return render(request,'front/cart.html',dic)

# 从购物车里面删除
@user_decorator.login_check
def delete_cart(request):
    cartId = request.GET.get('cartId', None)
    print(cartId)
    if cartId:
        cart = Cart.objects.get(id=int(cartId))
        cart.delete()
        return JsonResponse({'response': '1'})

@user_decorator.login_check
@user_decorator.check_session
def add_cart(request, dict_user):
    goodsID = request.GET.get('good_id', None)
    buyCount = request.GET.get('good_count', None)
    print(goodsID)
    print(buyCount)
    if goodsID and buyCount:
        name = request.session['username']
        user = C_UserInfo.objects.get(user_account=name)
        good = Goods.objects.get(gid=goodsID)
        cart = Cart.objects.filter(uid=user,gid=good)
        if len(cart) >=1:
            cart = cart[0]
            cart.counts = cart.counts+int(buyCount)
        else:
            cart = Cart()
            cart.uid =  user
            cart.gid = Goods.objects.get(gid=goodsID) # 这样反复的操作数据库不好吧
            cart.counts = int(buyCount)
        cart.save()
        number = user.cart_set.count()
        return JsonResponse({'number': number}) # 设置显示购物车中数量
    else:
        return  JsonResponse({'number': 0})
