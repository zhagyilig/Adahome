# coding=utf-8
# auth: zhangyiling
# time: 2018/9/16 下午10:29
# description:

import logging
import json
from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)

# 连接influxdb相关信息
infludbcon = {
    'host': '172.16.18.88',
    'port': 8086,
    'database': 'collectdb'
}


class InfluxdbGraphTemView(LoginRequiredMixin, TemplateView):
    """加载图形数据"""
    template_name = 'monitor/influxdb/influx_graph.html'

    def get_context_data(self, **kwargs):
        context = super(InfluxdbGraphTemView, self).get_context_data(**kwargs)
        try:
            client = InfluxClient()
            client.query()
            context['series'] = json.dumps(client.series)
            context['categories'] = client.categories
        except:
            pass

        return context


class InfluxdbApiView(LoginRequiredMixin, View):
    """influxdb api"""

    def get(self, request):
        ret = {}
        ret['status'] = 0
        client = InfluxClient()
        client.query()
        ret['categories'] = client.categories
        ret['series'] = client.series
        return JsonResponse(ret, safe=False)


class InfluxClient():
    """influxdb相关的操作"""

    def __init__(self):
        self.client = InfluxDBClient(host=infludbcon['host'], port=infludbcon['port'],
                                     database=infludbcon['database'], )
        self.categories = []  # x轴的数据
        self.series = []  # 图形数据点

    def query(self):
        """查询influxdb中的数据"""

        hostnames = ['study-zyl-node5', ]
        sql = ''  # 查询sql

        for hostname in hostnames:
            sql += '''select mean(value) as value from interface_tx \
where time > now() - 5m and instance = 'eth0' and type = 'if_octets' \
and host = '{}' group by time(10s) order by time desc; '''.format(hostname)

        print(sql)
        logger.debug('查询influxdb的sql是：{}'.format(sql))
        try:
            result = self.client.query(sql, epoch='s')
            # print('result: {}'.format(result))
        except Exception as e:
            logger.error('查询influxdb报错：{}'.format(e.args))

        for index, hostname in enumerate(hostnames):
            print(index, hostname)  # 0 study-zyl-node5
            self.process_data(hostname, result[index].get_points())

    def process_data(self, hostname, data_points):
        serie = {}
        serie['name'] = hostname
        serie['type'] = 'line'
        serie['data'] = []
        categories = []
        for point in data_points:
            serie['data'].insert(0, point['value'])
            categories.insert(0, point['time'])

        self.series.append(serie)
        if not self.categories:
            self.categories = categories
        print('时间: ', categories)
        print('数据: ', serie)
