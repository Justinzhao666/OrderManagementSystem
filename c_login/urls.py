# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^login_handle/$',views.login_handle),
]