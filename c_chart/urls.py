from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cart/$',views.cart),
    url(r'^delete_cart/$',views.delete_cart),
    url(r'^add_cart/$', views.add_cart),
]