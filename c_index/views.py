# -*- coding: utf-8 -*-
import hashlib

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from c_index import user_decorator
from c_index.models import *


# 首页展示活动商品
@user_decorator.check_session
def index(request, dict_user):
    # 设置 session
    cates = GoodCategory.objects.all().order_by('id')[0:5]
    # activities = ActivityType.objects.all().order_by('id') # 先不搞活动啥的了，只有商品和类别！以后再弄
    # 获取活动不为空的商品
    msgs = []
    for cate in cates:
        msgs.append({'cate': cate, 'indexgood': cate.goods_set.all().order_by('count_sell')[0:4]})
    # indexgoods = Goods.objects.filter()
    # note: 当我传入是字典和字典的时候怎么处理？
    # print(indexgoods)
    # 视频中是将数据全部分类查出来，然后list传过去的，因为页面被固定！ 没办法的时候我也这么干
    dict_all = dict(dict_user, **{'msgs': msgs})  # 合并两个字典
    return render(request, 'front/index.html', dict_all)

def pagTab(list1, pIndex, num):
    p = Paginator(list1, num)
    if pIndex == '' or pIndex == None:
        pIndex = '1'
    pIndex = int(pIndex)
    list2 = p.page(pIndex)
    plist = p.page_range
    return list2, plist, pIndex

# 产品分类筛选 : 这个东西确实存在数据库里面有点太费性能了，下次还是写死在页面吧！
@user_decorator.check_session
def list_category(request, dict_user, cate):
    if cate=='':
        goods = Goods.objects.all().order_by('cate_id_id')
        goodcount = goods.count()
        sub_cate = ''
    else:
        goods = Goods.objects.filter(cate_id_id=cate) # 商品
        goodcount = goods.count()
        if cate != '0':
            sub_cate = GoodCategory.objects.filter(id=cate).values()[0]['category']  # 垃圾代码
        else:
            sub_cate = '其他' # 副标题
    cates = GoodCategory.objects.all().order_by('id')[0:5] # 所有类别
    recom = Goods.objects.all().order_by('count_sell')[0:4]  # 3. 左侧推荐 商品销售数量决定
    pIndex = request.GET.get('page', None)
    # 单页商品list，一共分了多少页，当前的页码
    goods_page, page_num, pageindex = pagTab(goods, pIndex, 20)  # 分页(数据源，前端选择的页码，每页多少数据)
    pagenums = len(page_num)
    if len(page_num)>=5:   #页码显示页数 最多显示多少个页码
        if len(page_num)==pageindex:
            page_num=page_num[pageindex-3:pageindex]
        elif pageindex==1:
            page_num=page_num[0:pageindex+2]
        else:
            page_num=page_num[pageindex-2:pageindex+1]
    dict1 = {'cates': cates, 'goods': goods_page, 'sub_cate': sub_cate,'page_num':page_num,'pageindex':pageindex,
             'recom':recom,'pagenums':pagenums,'goodcount':goodcount}
    dict_all = dict(dict1, **dict_user)
    return render(request, 'front/list.html', dict_all)

def pagTab(list1, pIndex, num):
    '''
    分页函数
    '''
    p = Paginator(list1, num)
    if pIndex == '' or pIndex == None:
        pIndex = '1'
    pIndex = int(pIndex)
    list2 = p.page(pIndex)
    plist = p.page_range
    return list2, plist, pIndex

# 弃用
@user_decorator.check_session
def detail(request, dict_user):
    return render(request, 'front/detail.html', dict_user)

@user_decorator.login_check
@user_decorator.check_session
def user_center_info(request, dict_user):
    return render(request, 'front/user_center_info.html', dict_user)  # 宏观上的一个改法就是在html中写判断
# 用户修改自己信息使用 --后期将他给为 ajax传输  ----验证没做！ 前后都没做！
@user_decorator.login_check
def user_center_info_handle(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/user_center_info_handle/')
    post = request.POST
    first_name = post.get('firstname', '')
    second_name = post.get('secondname', '')
    gender = post.get('gender', '')
    telecom = post.get("telecom", '')
    phone = post.get("phone", '')
    company = post.get('company', '')
    address = post.get('address', '')
    user = C_UserInfo.objects.get(user_account=request.session['username'])
    user.user_firstname = first_name
    user.user_secondname = second_name
    user.user_gender = gender
    if gender == '女':
        user.user_pic = 'head/women.png'
    else:
        user.user_pic = 'head/man.png'
    user.user_telecom = telecom
    user.user_phone = phone
    user.user_company = company
    user.user_addr = address
    user.save()
    return HttpResponseRedirect('/user_center_info/')

@user_decorator.login_check
@user_decorator.check_session
def user_changepwd(request, dict_user):
    dict_error = {'errors': request.GET.get('errors', '修改您的密码，至少五位！')}
    dict_new = dict(dict_error, **dict_user)
    print(dict_new)
    return render(request, 'front/user_changepwd.html', dict_new)


# 修改密码： 1 原密码失败。2两次密码不一样 3 密码长度不适合 4 修改成功
@user_decorator.login_check
def changepwd_handle(request):
    post = request.POST
    pwd_old = post.get('pwd_old')
    pwd_new1 = post.get('newpwd1')
    pwd_new2 = post.get('newpwd2')
    print(pwd_new1)
    print(pwd_new2)
    if pwd_new1 != pwd_new2:
        # redirect 使用get方式传递url，然后再渲染模板的视图中添加get处理逻辑
        return HttpResponseRedirect('/user_changepwd/?errors=错误：两次密码不一致！')
    if len(pwd_new1) < 5 or len(pwd_new2) < 5:
        return HttpResponseRedirect('/user_changepwd/?errors=错误：新密码太短！')
    user = C_UserInfo.objects.get(user_account=request.session['username'])
    if hashlib.md5(pwd_old.encode(encoding='utf-8')).hexdigest() != user.user_pwd:
        return HttpResponseRedirect('/user_changepwd/?errors=错误：原密码不对！')
    user.user_pwd = hashlib.md5(pwd_new1.encode(encoding='utf-8')).hexdigest()
    user.save()
    return HttpResponseRedirect('/user_changepwd/?errors=修改成功')


# 退出登录
def logout(request):
    if request.session.get('username', default=None):
        del request.session['username']
    return HttpResponseRedirect('/index/')


# 商品详情页面
@user_decorator.check_session
def goodinfo(request, dict_user, id):
    good = Goods.objects.get(gid=id)
    cates = GoodCategory.objects.all().order_by('id')[0:5]
    dict1 = {'good': good,'cates':cates}
    dict_all = dict(dict1, **dict_user)
    return render(request, 'front/detail.html', dict_all)

# 用于搜搜
from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        return context