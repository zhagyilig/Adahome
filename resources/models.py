# coding=utf-8
# auth: zhangyiling

from django.db import models


# Create your models here.

class Idc(models.Model):
    """idc表"""
    name = models.CharField(max_length=32, default='', unique=True, verbose_name='机房名称首字母')
    idc_name = models.CharField(max_length=100, default='', verbose_name='机房名称')
    address = models.CharField(max_length=255, default='', verbose_name='机房地址')
    phone = models.CharField(max_length=25, default='', verbose_name='机房联系电话')
    email = models.EmailField(null=True, verbose_name='机房联系邮件')
    username = models.CharField(max_length=32, null=True, verbose_name='联系人')

    class Meta:
        db_table = 'resources_idc'
        # ordering=('-name')

    def __str__(self):
        '''
        django admin显示的字段
        :return:
        '''
        return self.idc_name


class Server(models.Model):
    """服务机器资产信息表"""
    supplier = models.IntegerField(null=True)
    manufacturers = models.CharField(max_length=50, null=True, verbose_name='产商')
    manufacture_date = models.DateField(null=True)
    server_type = models.CharField(max_length=20, null=True)
    sn = models.CharField(max_length=60, db_index=True, null=True)
    idc = models.ForeignKey(Idc, null=True)
    os = models.CharField(max_length=50, null=True)
    hostname = models.CharField(max_length=50, db_index=True, null=True)
    inner_ip = models.CharField(max_length=32, null=True, unique=True)  # 唯一
    mac_address = models.CharField(max_length=50, null=True)
    ip_info = models.CharField(max_length=255, null=True)
    server_cpu = models.CharField(max_length=250, null=True)
    server_disk = models.CharField(max_length=100, null=True)
    server_mem = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, db_index=True, null=True)
    remark = models.TextField(null=True)
    service_id = models.IntegerField(db_index=True, null=True)
    server_purpose = models.IntegerField(db_index=True, null=True)
    check_update_time = models.DateTimeField(auto_now=True, null=True)  # auto_now 自动更新时间
    vm_status = models.IntegerField(db_index=True, null=True)
    uuid = models.CharField(max_length=100, db_index=True, null=True)

    def __str__(self):
        return "{} [{}]".format(self.hostname, self.inner_ip)

    class Meta:
        db_table = 'resources_server'
        ordering = ['id']


class Product(models.Model):
    """业务线表"""
    service_name = models.CharField("业务线的名字", max_length=32)
    module_letter = models.CharField("业务线字母简称", max_length=10, db_index=True)
    op_interface = models.CharField("运维负责人", max_length=150)
    dev_interface = models.CharField("业务负责人", max_length=150)
    pid = models.IntegerField("上级业务线id", db_index=True)

    def __str__(self):
        return self.service_name

    class Meta:
        db_table = 'resources_product'
        ordering = ['id']
