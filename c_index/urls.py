from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$',views.index),
    url(r'^list/(?P<cate>\d*)$',views.list_category),
    url(r'^list/(?P<cate>[0-9]+)/$',views.list_category),
    url(r'^user_center_info/$',views.user_center_info),
    url(r'^user_center_info_handle/$',views.user_center_info_handle),
    url(r'^user_changepwd/$',views.user_changepwd),
    url(r'^changepwd_handle/',views.changepwd_handle),
    url(r'^logout/$',views.logout),
    url(r'^detail/(?P<id>[0-9a-zA-Z\-]+)/$',views.goodinfo),

]