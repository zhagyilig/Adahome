# coding=utf-8
# author: zhangyiling


from django.conf.urls import include, url
from . import zabbix, influxdb

urlpatterns = [
    url(r'^zabbix/', include([
        url(r'^cachehost/$', zabbix.ZabbixCacheHostView.as_view(), name="zabbix_cachehost"),  # 缓存表
    ])),

    url(r'^influx/', include([
        url('^get/$', influxdb.InfluxdbApiView.as_view(), name='influx_api'),
        url('^echart/$', influxdb.InfluxdbGraphTemView.as_view(), name='influx_graph'),

    ]))
]
