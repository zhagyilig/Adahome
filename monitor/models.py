# coding=utf-8
# auth: zhangyiling

from django.db import models
from resources.models import Server, Product


# Create your models here.

class ZabbixHost(models.Model):
    """zabbix缓存主机列表"""
    hostid = models.IntegerField('zabbix hostid', db_index=True)
    host = models.CharField('zabbix hostname', max_length=50, null=True)
    ip = models.CharField('zabbix ip', max_length=32, db_index=True)
    server = models.OneToOneField(Server)
    updatetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.hostid, self.host)

    class Meta:
        db_table = 'zabbix_cache_host'
        ordering = ['id']

    # ex: zhhosts: [{'hostid': '10084', 'host': '172.16.18.88', 'ip': '172.16.18.88'}]


class Graph(models.Model):
    """图形管理表"""
    title = models.CharField(max_length=50, null=False, verbose_name='图形标题')
    subtitle = models.CharField(max_length=50, null=True, verbose_name='图形子标题')
    unit = models.CharField(max_length=10, null=False, verbose_name='数据点格式化后的单位')
    measurement = models.CharField(max_length=32, null=False, verbose_name='influxdb的表名')
    auto_hostname = models.BooleanField(default=True, null=False, verbose_name='是否从业务线取主机名作为条件')
    field_expression = models.CharField(max_length=120, null=True, verbose_name='influxdb sql的where条件')
    product = models.ManyToManyField(Product, verbose_name='与业务线表多对多关联')
    tootip_formatter = models.CharField(max_length=100, null=True, verbose_name='对echarts的tooltip进行格式化')
    yaxis_formatter = models.CharField(max_length=100, null=True, verbose_name='对echarts的y轴进行格式化')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'monitor_influx_graph'
        ordering  = ['id']