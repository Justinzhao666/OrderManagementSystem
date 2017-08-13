# coding=utf-8
from django.db import models
from tinymce.models import HTMLField
# Create your models here.

## 客户表
class C_UserInfo(models.Model):
    user_account = models.CharField(max_length=20,unique=True,db_index=True,primary_key=True,verbose_name='用户名')    # 账户
    user_pwd = models.CharField(max_length=50)                                                                         # 密码
    user_pic = models.ImageField(upload_to='head/',default='head/man.png')                       # 头像
    user_gender = models.CharField(verbose_name='性别',choices=(('男','男'),('女','女')),max_length=1,null=True) #性别
    user_firstname = models.CharField(max_length=20,default='',blank=True,verbose_name='姓')                            # 姓
    user_secondname = models.CharField(max_length=20,default='',blank=True,verbose_name='名')                           # 名
    user_telecom = models.CharField(max_length=11,blank=True,null=True,default='')      # 固话
    user_phone =  models.CharField(max_length=11,verbose_name='手机')                            # 手机
    user_company= models.CharField(max_length=50,blank=True,null=True,default='')          # 公司名称
    user_addr = models.CharField(max_length=100,blank=True,null=True,default='')                                # 用户地址
    user_lastlogin = models.DateTimeField(null=True,verbose_name='上次登录')                 # 上次登录时间
    isdelete = models.BooleanField(default=False)                               # 删除用户
    class Meta():
        verbose_name = '客户表'
        verbose_name_plural = '客户表' #admin视图的表名
        db_table = 'my_users'
    def __str__(self):
        return str(self.user_account)

## 管理员表
class B_Admin(models.Model):
    username = models.CharField(max_length=20,primary_key=True) # 管理员账户
    password = models.CharField(max_length=50)                  # 密码
    last_login = models.DateTimeField()                         # 上次登录时间
    class Meta():
        verbose_name = '管理员表'
        verbose_name_plural = '管理员表'
        db_table = 'my_admin'
    def __str__(self):
        return str(self.username)

# 供应商表
class B_Supplier(models.Model):
    company = models.CharField(max_length=100)      # 供应商公司名
    principal = models.CharField(max_length=20)     # 供应商负责人
    telecom = models.CharField(max_length=11)    # 电话
    phone = models.CharField(max_length=11)      # 手机
    address = models.CharField(max_length=100)      # 地址
    notes = models.TextField()                      # 备注
    class Meta():
        verbose_name = '供应商表'
        verbose_name_plural = '供应商表'
        db_table = 'my_suppliers'
    def __str__(self):
        return str(self.company)

## 首页活动类型
class ActivityType(models.Model):
    id = models.AutoField(primary_key=True)         # 首页有哪些活动的id
    category = models.CharField(max_length=20)      # 活动名字
    class Meta():
        verbose_name = '首页活动类型表'
        verbose_name_plural = '首页活动类型表'
        db_table = 'my_activtytype'
    def __str__(self):
        return str(self.category)

## 首页大条幅商品设置
class IndexPageGoods(models.Model):
    good_id = models.ForeignKey('Goods')              # 商品id
    pic = models.ImageField(upload_to='goods/')       # 海报图片
    desc = models.CharField(max_length=50)            # 商品描述
    class Meta():
        verbose_name = '首页活动商品表'
        verbose_name_plural = '首页活动商品表'
        db_table = 'my_indexpagegoods'
    def __str__(self):
        return str(self.good_id)


## 商品的类别表
class GoodCategory(models.Model):
    id = models.AutoField(primary_key=True)                             # 商品类别id
    category = models.CharField(max_length=20,verbose_name='类别',unique=True)          # 商品类别名
    # isdelete = models.BooleanField(default=False)       # 商品类别是否被删除，考虑到暂时不买这东西
    class Meta():
        verbose_name = '商品类别表'
        verbose_name_plural = '商品类别表'
        db_table = 'my_goodcategory'
    def __str__(self):
        return str(self.category)


## 商品表
class Goods(models.Model):
    gid = models.CharField(max_length=20,primary_key=True,db_index=True)   # 商品编号(索引)
    good_name = models.CharField(max_length=20,db_index=True)                 # 商品名字（索引）
    cate_id = models.ForeignKey('GoodCategory')                # 商品类别
    count = models.PositiveIntegerField(default=0)                  # 商品库存
    unit = models.CharField(max_length=10)                      # 商品单位
    price_sell = models.DecimalField(max_digits=10,decimal_places=2)                # 商品售价
    price_orgin = models.DecimalField(max_digits=10,decimal_places=2)               # 商品原价
    good_shortinfo = models.TextField(null=True,default=' ')                         # 商品的简要说明
    good_info = HTMLField()                                     # 商品详解介绍
    good_pic = models.ImageField(upload_to='goods/')            # 商品图片
    good_activity = models.ForeignKey('ActivityType',null=True) # 商品的活动类别
    count_sell = models.IntegerField(default=0)                 # 商品的销量
    isdelete = models.BooleanField(default=False)               # 商品是否被删除
    class Meta():
        verbose_name = '商品表'
        verbose_name_plural = '商品表'
        db_table = 'my_goods'
    def __str__(self):
        return str(self.good_name)

## 订单表
class Orders(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)            # 订单编号
    uid = models.ForeignKey('C_UserInfo')               # 用户id
    state = models.CharField(max_length=20)             # 状态：待付款 待发货 待确认收货 完成
    time_begin = models.DateTimeField(null=True)                 # 下单日期
    time_end = models.DateTimeField(null=True)                   # 完成日期
    notes = models.TextField(null=True)                          # 订单备注信息*
    score = models.IntegerField(null=True)                       # 管理员对该订单印象
    pay = models.CharField(max_length=10,null=True)               # 付款方式
    isdelete = models.BooleanField(default=False)       # 是否删除,逻辑删除
    isdebt = models.BooleanField(default=False)         # 是否欠款：如果欠款需特殊标记来强调
    orgintotal = models.DecimalField(max_digits=10, decimal_places=2,null=True) # 订单利润
    ototal = models.DecimalField(max_digits=10, decimal_places=2,null=True) # 订单总金额
    address = models.CharField(max_length=100,blank=True,null=True,default='')  # 订单地址
    class Meta():
        verbose_name = '订单表'
        verbose_name_plural = '订单表'
        db_table = 'my_orders'
    def __str__(self):
        return str(self.oid)

# 订单详情表： 一个订单可能有多件商品,这里针对订单号每条商品的信息！
class OrderInfo(models.Model):
    oid = models.ForeignKey(Orders)
    gid = models.ForeignKey(Goods)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    count=models.IntegerField()
    class Meta():
        verbose_name = '订单详情'
        verbose_name_plural = '订单详情'
        db_table = 'my_orderInfo'
    def __str__(self):
        return str(self.oid)

# 购物车表
class Cart(models.Model):
    uid = models.ForeignKey('C_UserInfo')    # 用户id
    gid = models.ForeignKey('Goods')                  # 商品id
    counts = models.IntegerField(default=1)             # 加入购物车数量
    class Meta():
        verbose_name = '购物车表'
        verbose_name_plural = '购物车表'
        db_table = 'my_cart'
    def __str__(self):
        return str(self.uid)

# 进货表
class Purchases(models.Model):
    id = models.CharField(max_length=20,primary_key=True)             # 进货单号
    supplierId = models.ForeignKey('B_Supplier')  # 供应商id
    gid = models.ForeignKey('Goods')                  # 商品id
    time = models.DateTimeField()                       # 进货时间
    counts = models.IntegerField()                      # 进货数量
    money = models.DecimalField(max_digits=7,decimal_places=2)                       # 订单总价
    pay = models.DecimalField(max_digits=7,decimal_places=2)                         # 订单实付
    notes = models.TextField()                          # 订单备注
    class Meta():
        verbose_name = '进货表'
        verbose_name_plural = '进货表'
        db_table = 'my_purchase'
    def __str__(self):
        return str(self.goodsName)
