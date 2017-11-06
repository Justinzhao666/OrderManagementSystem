# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^place_order/$', views.place_order), #palce order 就是处理提交订单的
    url(r'^user_center_order/$',views.user_center_order),
    url(r'^order_handle/$',views.order_handle),
    url(r'^delete_order/$',views.delete_order),
]