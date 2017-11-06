# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from c_index.models import *


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user_account','user_firstname','user_secondname','user_gender','user_phone','user_lastlogin'] #
    # admin中数据表显示哪些字段
    list_filter = ['user_account'] # 按照哪个字段进行过滤来进行筛选
    search_fields = ['user_account'] # 数据表上会有一个搜索框来根据指定字段进行搜索
    list_per_page = 20 # 数据展示的分页
    ## 编译单条数据的配置 fields与fieldsets两者选一
    # fields = ['user_account', 'user_firstname'] # 表中单条数据显示哪些字段
    # fieldsets = [、
    #     ('basic', {'fields': ['user_account']}),
    #     ('more', {'fields': ['user_phone']}),
    # ] # 表中单条数据的属性进行分组
admin.site.register(C_UserInfo,UserInfoAdmin)

admin.site.register(B_Admin)
admin.site.register(B_Supplier)

admin.site.register(ActivityType)

class IndexpageGoodsAdmin(admin.ModelAdmin):
    list_display = ['id','good_id_id']

admin.site.register(IndexPageGoods,IndexpageGoodsAdmin)

class GoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
admin.site.register(GoodCategory,GoodCategoryAdmin)

class GoodAdmin(admin.ModelAdmin):
    list_display = ['gid','good_name','cate_id','count','unit','price_sell','price_orgin','good_pic','isdelete']
    list_filter = ['cate_id']
admin.site.register(Goods,GoodAdmin)
admin.site.register(Orders)
admin.site.register(Cart)
admin.site.register(Purchases)