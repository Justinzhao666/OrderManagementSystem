import datetime
import uuid

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from c_index import user_decorator
from c_index.models import *

# 这个千万不要从前台去读数据来操作！，当用户浏览器返回的时候再点击下单的时候，会一直增加订单！这不科学
from c_index.views import pagTab


# 处理购物车的商品  1 获取购物车的数据，2 查看是否大于库存(undo) 传递给place_order页面 / 点击立即购买的，
@user_decorator.login_check
@user_decorator.check_session
def place_order(request, dict_user):
    # 需要勾选商品的id，数量
    cartId = []
    if request.method == 'GET':  # 如果是立即购买的话
        count = request.GET.get('count', None)
        goodId = request.GET.get('id', None)  # 被勾选的商品的id
        agood = Goods.objects.get(gid=goodId)
        # print('-----count:' + count)
        # print('-----goodID:' + goodId)
        # print('-----goodID:' + str(type(goodId)))
        # 判断是否大于库存：
        if agood.count < int(count):
            return HttpResponse('你所要购买的商品 - ' + agood.good_name + ' - 库存不足！')
        goodId = [agood]  # 列表中只有一个商品
        count = [count]
    # 从购物车中提交的
    elif request.method == 'POST':
        count = request.POST.getlist('count', None)  # 这里是购物车里面的数据量
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
            # print('goodID:' + str(goodId))  # 里面存放的是good对象
    else:
        pass
    # 上面造出了 goodID 的list  和 count 的list
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
        'orderlist': orderlist,  #
        'allprice': sumprice + freight,
        'freight': freight,
        'goodsamount': len(goodId),  # 商品总数
        'alltotal': sumprice,
        'cartId': cartId,
    })
    return render(request, 'front/place_order.html', dic)


# 订单数据存入数据库操作！ ************
@transaction.atomic()
@user_decorator.login_check
def order_handle(request):
    # 处理订单： 获取订单信息，检验库存，插入order，删除购物车，跳转到用户订单页面（事物）
    tran_id = transaction.savepoint()
    try:
        addr = request.POST.get('address')  # 获取地址
        if addr == '':
            transaction.savepoint_rollback(tran_id)
            return HttpResponse('地址不可以为空！')
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
        orgintotal = 0  # 订单的成本价
        if cartIdList[0]:  # 如果是从购物车中的订单,就不要从前端去读，而是从购物车去读，因为在前一个页面购物车就已经被更新为用户所修改的了
            for i in cartIdList:
                oinfo = OrderInfo()
                cart = Cart.objects.get(id=int(i))
                goods = cart.gid  # 这里直接就是good对象
                # 判断库存：
                if cart.counts <= goods.count:  # 可以购买
                    goods.count = goods.count - cart.counts  # 修改库存
                    goods.save()  # 修改库存
                    oinfo.oid = order
                    oinfo.gid = goods
                    oinfo.price = goods.price_sell
                    oinfo.count = cart.counts
                    oinfo.save()
                    total = total + oinfo.price * oinfo.count
                    orgintotal = orgintotal + oinfo.gid.price_orgin * oinfo.count
                    cart.delete()  # 删除购物车中的商品
                else:
                    # 失败回滚并返回到购物车
                    transaction.savepoint_rollback(tran_id)
                    return HttpResponse('你所购买产品 - ' + goods.good_name + ' - 库存不足！')
            order.ototal = total
            order.orgintotal = orgintotal - total
            order.save()
            transaction.savepoint_commit(tran_id)
        else:  # 点击立即购买的，只有一种商品 这里的数量name牵扯到其他模块
            # for agood in goodsId: # 应该使用一个tuple来包装 good - count
            goods = Goods.objects.get(gid=goodsId[0])
            if int(goodscount[0]) <= goods.count:  # 可以购买
                goods.count = goods.count - int(goodscount[0])
                goods.save()  # 修改库存
                oinfo = OrderInfo()
                oinfo.gid = goods
                oinfo.price = goods.price_sell
                oinfo.oid = order
                oinfo.count = int(goodscount[0])
                oinfo.save()
                total = total + oinfo.price * oinfo.count
                orgintotal = orgintotal + oinfo.gid.price_orgin * oinfo.count
            else:
                # 失败回滚并返回到购物车
                transaction.savepoint_rollback(tran_id)
                return HttpResponse('你所购买产品库存不足！')
            order.ototal = total
            order.orgintotal = orgintotal - total
            order.save()
            transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('订单发生异常！' + str(e))
        transaction.savepoint_rollback(tran_id)
    return redirect('/user_center_order/')  # 转至订单页面


# 显示用户的订单
@user_decorator.login_check
@user_decorator.check_session
def user_center_order(request, dict_user):
    # 先处理为取消订单不显示，后续在具体人性化处理
    order_list = Orders.objects.filter(uid=request.session['username'], ).filter(isdelete=False).order_by('-oid')
    pIndex = request.GET.get('page', None)  # 获取页面index
    if pIndex == '' or pIndex == None:
        pIndex = '1'
    pIndex = int(pIndex)
    # 单页list 页数 给定页码
    page_orders, page_count, page_no = pagTab(order_list, pIndex, 4)  # 分页 源数据 前端页码， 每页的数据
    pagenums = len(page_count)
    if len(page_count) >= 5:  # 页码显示页数
        if len(page_count) == pIndex:
            page_count = page_count[pIndex - 3:pIndex]
        elif pIndex == 1:
            page_count = page_count[0:pIndex + 2]
        else:
            page_count = page_count[pIndex - 2:pIndex + 1]
    # 针对单个订单的商品详情：
    orders = []
    for order in page_orders:  # 取出一个订单，查出它的所有商品
        detaillist = []
        for i in order.orderinfo_set.all():  # 一个个的商品记录
            detaillist.append({'goodrecord': i})
        orders.append({'order': order, 'orderdetail': detaillist})
    dic = dict(dict_user, **{
        'orderlist': orders,
        'plist': page_count,
        'pIndex': pIndex,
        'pagenums': pagenums
    })
    return render(request, 'front/user_center_order.html', dic)


# 用户取消订单 ***************
@transaction.atomic()
@user_decorator.login_check
@user_decorator.check_session
def delete_order(request, dict_user):
    tran_id = transaction.savepoint()
    try:
        # 1 检验是否已经发货， 可以取消： 删除订单表记录（逻辑删除），将库存加回去，
        orderid = request.GET.get('order', None)
        if orderid == '':
            transaction.savepoint_rollback(tran_id)
            return HttpResponse('非法操作！')
        order = Orders.objects.get(oid=orderid)
        if order:
            if order.state != "待发货":  # 防止恶意攻击
                return HttpResponse('非法操作！')
            # 删除表中order记录
            order.isdelete = True
            order.state = 'deleted'
            order.save()
            print('删除成功')
            # 恢复库存
            for item in order.orderinfo_set.all():
                good = item.gid
                good.count = good.count + item.count
                good.save()
                print('库存保存成工')
            transaction.savepoint_commit(tran_id)
            return redirect('/user_center_order/')
        else:
            transaction.savepoint_rollback(tran_id)
            return HttpResponse('非法操作！')
    except Exception as e:
        print('订单取消失败' + str(e))
        transaction.savepoint_rollback(tran_id)
        return HttpResponse('订单取消失败！')
