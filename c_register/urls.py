# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$',views.register,name='login'),
    url(r'^register_handle/$',views.register_handle),
    url(r'^usercheck/$',views.usercheck),
]