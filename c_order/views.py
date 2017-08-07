import datetime
import uuid

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from c_index import user_decorator
from c_index.models import *

# 这个千万不要从前台去读数据来操作！，当用户浏览器返回的时候再点击下单的时候，会一直增加订单！ 这不科学
@transaction.atomic()
@user_decorator.login_check
def order_handle(request):
    #处理订单： 获取订单信息，检验库存，插入order，删除购物车，跳转到用户订单页面（事物）
    tran_id = transaction.savepoint()
    try:
        addr = request.POST.get('address')  # 获取地址
        goodscount = request.POST.getlist('goodscount')  # 获取商品数量
        # print('goodscount:' + str(goodscount))  # ['8', '4', '1', '1']
        goodsId = request.POST.getlist('goodsId')  # 获取商品的id
        # print('goodid:' + str(goodsId))  #
        cartIdList = request.POST.getlist('cartId')  # 如果是购物车结算的的获取购物车id，需要删除的id
        # print('cartid:' + str(cartIdList))  # ['12', '14', '15', '16']
        notes = request.POST.get('notes')
        now = datetime.datetime.now()
        uid = C_UserInfo.objects.get(user_account=request.session['username'])
        print('uid' + str(uid))
        # 设置订单
        order = Orders()
        order.oid = now.strftime('%Y%m%d%H%M%S') + '-' + str(uuid.uuid1()).replace('-', '')[0:5]
        order.uid = uid
        order.state = '待发货'
        order.time_begin = now
        order.notes = notes
        order.pay = '货到付款'
        order.isdelete = False
        order.isdebt = False
        order.address = addr  # 订单指定的地址
        order.save()
        # 插入订单详情
        total = 0  # 订单总额
        if cartIdList[0]:  # 如果是从购物车中的订单
            for i in cartIdList:
                oinfo = OrderInfo()
                cart = Cart.objects.get(id=int(i))
                goods = cart.gid  # 这里直接就是good对象
                # 判断库存：
                if cart.counts <= goods.count:  # 可以购买
                    goods.count = goods.count - cart.counts
                    goods.save()  # 修改库存
                    oinfo.oid = order
                    oinfo.gid = goods
                    oinfo.price = goods.price_sell
                    oinfo.count = cart.counts
                    oinfo.save()
                    total = total + oinfo.price * oinfo.count
                    cart.delete()  # 删除购物车中的商品
                else:
                    # 失败回滚并返回到购物车
                    transaction.savepoint_rollback(tran_id)
                    return redirect('/cart/')
            order.ototal = total
            order.save()
            transaction.savepoint_commit(tran_id)
        else: # 点击立即购买的，只有一件商品 这里的数量name牵扯到其他模块
            goods = Goods.objects.get(gid=int(goodsId))
            if int(goodscount[0]) <= goods.count:  # 可以购买
                oinfo = OrderInfo()
                oinfo.gid = goods
                oinfo.price = goods.price_sell
                oinfo.oid = order
                oinfo.count = goodscount[0]
                oinfo.save()
                total = total + oinfo.price*oinfo.count
            else:
                # 失败回滚并返回到购物车
                transaction.savepoint_rollback(tran_id)
                return HttpResponse('你所购买产品库存不足！')
            order.ototal = total
            order.save()
            transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('订单发生异常！')
        transaction.savepoint_rollback(tran_id)
    return render(request, 'front/user_center_order.html')


# 处理购物车的商品  1 获取购物车的数据，2 查看是否大于库存 传递给place_order页面
@user_decorator.login_check
@user_decorator.check_session
def place_order(request, dict_user):
    # 需要勾选商品的id，数量
    cartId = []
    if request.method == 'GET':  # 如果是立即购买的话
        count = request.GET.get('count', None)
        goodId = request.GET.get('id', None)  # 被勾选的商品的id
        goodId = [goodId]
    elif request.method == 'POST':
        count = request.POST.getlist('count', None)  # 这里是购物车的数据量
        cartId = request.POST.getlist('id', None)  # 购物车表的id
        # 已获取到购物车的id 和数量，然后根据购物车的数量确定商品的id
        goodId = []
        j = 0  # 一个计数器
        for i in cartId:
            cart = Cart.objects.get(id=int(i))
            goodId.append(cart.gid)
            if int(count[j]) != cart.counts:  # 如果发现购物车的数量不一致，先更新一下数量，soga！在这里验证
                cart.counts = int(count[j])
                cart.save()
            j += 1
        print('goodID:' + str(goodId))  # 里面存放的是good对象
    else:
        pass
    orderlist = []
    freight = 0  # 运费
    sumprice = 0
    # 构造商品列表，并计算总价
    for i in range(len(goodId)):
        goods = goodId[i]
        orderdic = {'goods': goods, 'count': i + 1, 'sumtotal': goods.price_sell * int(count[i]),
                    'goodscount': count[i]}
        if len(cartId) > 0:  # 加入购物车的id--商品所对应的购物车
            orderdic['cartId'] = cartId[i]
        orderlist.append(orderdic)
        sumprice += goods.price_sell * int(count[i])  # 统计总价 所有商品的
    dic = dict(dict_user, **{
        # 'AddrList': AddrList,不需要地址，这个user对象本身就会传递前台
        'orderlist': orderlist,
        'allprice': sumprice + freight,
        'freight': freight,
        'goodsamount': len(goodId),  # 商品总数
        'alltotal': sumprice,
        'cartId': cartId,
    })
    return render(request, 'front/place_order.html', dic)


@user_decorator.login_check
@user_decorator.check_session
def user_center_order(request, dict_user):
    return render(request, 'front/user_center_order.html', dict_user)
