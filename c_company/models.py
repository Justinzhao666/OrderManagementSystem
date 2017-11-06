# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
## 公司信息
class CompanyInfo(models.Model):
    address = models.CharField(max_length=100)      # 自己公司简介
    contact = models.CharField(max_length=11)    # 自己公司联系方式
    info = models.TextField()                       # 自己公司信息
    class Meta():
        verbose_name = '我的公司信息表'
        verbose_name_plural = '我的公司信息表'
        db_table = 'my_company_info'
    def __str__(self):
        return str(self.address)