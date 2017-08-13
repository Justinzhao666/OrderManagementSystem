from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^OMS_admin/blogin/$',views.blogin),
]