# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^OMS_admin/blogin/$',views.blogin),
    url(r'^blogin_handle/$',views.blogin_handle),
    url(r'^admin_logout/$',views.admin_logout),
]