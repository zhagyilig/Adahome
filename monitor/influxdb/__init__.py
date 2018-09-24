# coding=utf-8
# auth: zhangyiling
# time: 2018/9/16 下午10:29
# description:

import logging
import json
import time
from django.http import JsonResponse
from django.views.generic import TemplateView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.http import urlquote_plus  # url编码
from influxdb import InfluxDBClient
from monitor.forms import CreateGraphForm
from monitor.models import Graph

logger = logging.getLogger(__name__)

# 连接influxdb相关信息
infludbcon = {
    'host': '172.16.18.88',
    'port': 8086,
    'database': 'collectdb'
}

'''
第一部分: 系统新能展示
'''


class InfluxdbGraphTemView(LoginRequiredMixin, TemplateView):
    """加载图形数据"""
    template_name = 'monitor/influxdb/influx_graph.html'

    def get_context_data(self, **kwargs):
        """加载前端图形数据"""
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
    """influxdb api, 获取influxdb的数据"""

    def get(self, request):
        ret = {}
        ret['status'] = 0
        client = InfluxClient()
        client.query()
        ret['series'] = client.series  # 图表数据
        ret['categories'] = client.categories  # x轴数据
        return JsonResponse(ret, safe=False)


class InfluxClient():
    """influxdb相关操作"""

    def __init__(self):
        self.client = InfluxDBClient(host=infludbcon['host'], port=infludbcon['port'],
                                     database=infludbcon['database'], )
        self.categories = []  # x轴的数据
        self.series = []  # 图形数据点
        self.measurements = self.get_measurements()

    def query(self):
        """查询influxdb中的数据"""

        hostnames = ['study-zyl-node5', 'zyl-node1', ]
        # hostnames = ['zyl-node1', 'zyl-node2', ]
        sql = ''  # 查询sql
        for hostname in hostnames:
            sql += '''select mean(value) as value from memory_value \
where time > now() - 15m and type_instance = 'free' and type = 'memory' \
and host = '{}' group by time(60s) order by time desc; '''.format(hostname)
        logger.debug('查询influxdb的sql是：{}'.format(sql))
        try:
            result = self.client.query(sql, epoch='s')  # 返回查出的数据
            logger.debug('查出的数据: {}'.format(result))

        except Exception as e:
            logger.error('查询influxdb报错：{}'.format(e.args))

        for index, hostname in enumerate(hostnames):
            # print(index, hostname)  # 0 study-zyl-node5
            self.process_data(hostname, list(result[index])[0])  # list(ret[1])[0]

    def process_data(self, hostname, data_points):
        """处理数据：
        拿到主机名和数据
        """
        serie = {}
        serie['name'] = hostname  # 系列名称，用于tooltip的显示
        serie['type'] = 'line'  # 折线图
        serie['data'] = []
        categories = []  # x轴
        for point in data_points:
            serie['data'].insert(0, point['value'])
            categories.insert(0, point['time'])

        self.series.append(serie)
        if not self.categories:
            self.categories = self.process_time(categories)

        logger.debug('时间: {} '.format(categories))
        logger.debug('数据: {}'.format(serie))

    def process_time(self, categories):
        """处理前端显示时间"""
        ret = []
        format_str = "%Y%m%d %H:%M:%S"
        for point in categories:
            ret.append(time.strftime(format_str, time.localtime(point)))
        return ret

    def get_measurements(self):
        """获取influx所有的表"""
        measurements = self.client.query('show measurements').get_points()
        '''
        In [7]: mea = clent.query('show measurements').get_points()
        In [8]: mea
        Out[8]: <generator object ResultSet.get_points at 0x7febaf832258>

        In [9]: for n  in mea:
           ...:     print(n)
           ...:
        {'name': 'cpu_value'}
        {'name': 'df_free'}
        {'name': 'df_used'}
        ....
        '''
        return [n['name'] for n in measurements]


'''
第二部分: 图形管理 20180923
'''


class CreateGraphTemView(LoginRequiredMixin, TemplateView):
    """创建图形，并验证表单"""
    template_name = 'monitor/influxdb/create_graph.html'

    def get_context_data(self, **kwargs):
        """前端加载数据，获取influx的表(measurements)"""
        context = super(CreateGraphTemView, self).get_context_data(**kwargs)
        try:
            client = InfluxClient()
            context['measurements'] = client.measurements
        except Exception as e:
            logger.error('获取influx中的表的失败: {}'.format(e.args))
        logger.debug('获取influx中的表成功')
        return context

    def post(self, request):
        """获取提交的数据，并验证"""
        logger.debug('创建图形: {},操作人: {}'.format(request.POST, request.user))
        next_url = urlquote_plus(
            request.GET.get('next', None) if request.GET.get('next', None) else reverse('influx_graph_list'))
        form = CreateGraphForm(request.POST)
        if form.is_valid():
            try:
                graph = Graph(**form.cleaned_data)
                graph.save()
                return redirect('success', kwargs={'next': next_url})
            except Exception as e:
                logger.error('创建图形保存数据库失败: {}'.format(e.args))
                return redirect("error", next=next_url, msg=e.args)
        else:
            logger.error('表单数据验证失败.')
            return redirect("error", next=next_url, msg=form.errors.as_json())


class GraphListView(LoginRequiredMixin, ListView):
    """图形管理列表"""
    template_name = 'monitor/influxdb/graph_list.html'
    model = Graph
    paginate_by = 10
    ordering = 'id'
