# -*- coding: utf-8 -*-
"""OrderManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from OrderManagementSystem import settings
from c_index import views

urlpatterns = [
    url(r'^$', views.index),  # 直接进入首页
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('c_login.urls')),
    url(r'^', include('c_register.urls')),
    url(r'^', include('c_index.urls')),
    url(r'^', include('c_chart.urls')),
    url(r'^', include('c_order.urls')),
    url(r'^', include('b_home.urls')),
    url(r'^', include('b_login.urls')),
    # url(r'^search/', include('haystack.urls')),
    # url(r'^search/', views.MySearchView.as_view()),

]

# 让 Django 给通过开发服务器上传的媒体文件提供服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
