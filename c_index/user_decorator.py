from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from c_index.models import *

# 检验是否登录
def login_check(fun):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('username'):
            return fun(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return JsonResponse({'login':'no'})
            else:
                ret = HttpResponseRedirect('/login/')
                ret.set_cookie('url_tmp',request.get_full_path())
                return ret
    return login_fun

# 检验连接是否有session，如果有的话就显示在页面顶端，主要用于传递显示于页眉的数据
def check_session(fn):
    def wrapper(request,**kwargs):
        # 获取session
        username = request.session.get('username')
        user = ''
        cart_num = 0
        if username:
            user = C_UserInfo.objects.get(user_account=username) # 获取user对象
            cart_num = user.cart_set.all().count()
        dict = {'user':user,'cart_num':cart_num}
        ret = fn(request,dict,**kwargs)
        return ret
    return wrapper