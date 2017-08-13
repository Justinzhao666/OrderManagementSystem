from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^homepage/$',views.homepage),
    # 用户
    url(r'^admin_user_all/$',views.admin_user_all),
    url(r'^admin_user_edit/$',views.admin_user_edit),
    url(r'^admin_user_add/$',views.admin_user_add),
    url(r'^admin_user_save/$',views.admin_user_save),
    # 订单
    url(r'^admin_order/(?P<cate>[0-9])/$',views.admin_order), # 显示订单列表
    url(r'^admin_showorder/$',views.admin_showorder), # 显示订单详情
    url(r'^admin_change_order_state/$',views.admin_change_order_state), # 点击改变状态
    url(r'^admin_reportorder/$',views.admin_reportorder), # 点击改变状态
    # 商品
    url(r'^admin_good_all/$', views.admin_good_all),  # 显示所有的商品信息
    url(r'^admin_good_info/$',views.admin_good_info),
    url(r'^admin_good_save/$',views.admin_good_save),
    url(r'^admin_good_add/$',views.admin_good_add),
    url(r'^gid_check/$',views.gid_check),
    url(r'^user_check/$',views.user_check),

]