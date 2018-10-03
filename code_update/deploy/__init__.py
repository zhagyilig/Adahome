# coding=utf-8
# auth: zhangyiling
# time: 2018/9/13 下午8:33
# description: 代码发布，回退相关功能


import time
import datetime
import logging
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin  # 登陆验证
from django.http import JsonResponse, QueryDict
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import RequestContext
from code_update.models import ServicesName
from resources.models import Server, Product
from core.saltapi import SaltApi
from core.mysql import DB_Operate

logger = logging.getLogger(__name__)

# salt return
RETURNS_MYSQL = {"host": "172.16.18.88",
                 "port": 9036,
                 "database": "salt",
                 "user": "zyl",
                 "password": "888888",
                 }


class CodeDeployTemView(LoginRequiredMixin, TemplateView):
    """代码发布"""
    template_name = 'code_update/deploy.html'

    # 需要自定义method的方式
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'search', ]

    def get_context_data(self, **kwargs):
        """加载所有的项目及服务列表"""
        context = super(CodeDeployTemView, self).get_context_data(**kwargs)
        # context['servernames'] = ServicesName.objects.all()  # 项目名列表
        # context['product'] = Product.objects.filter(service_name__icontains='detalase')  # 业务线，暂时写死了
        context['product'] = Product.objects.filter(pid=0)  # 业务线，暂时写死了
        context['project'] = Product.objects.all().exclude(pid=0)  # 部署项目
        context['serverlists'] = Server.objects.filter(hostname__icontains='node')  # 服务器列表

        logging.debug('加载所有的项目成功: {}'.format(context))
        return context

    def post(self, request):
        """获取前端提交的项目，并发布项目"""
        ret = ''
        host = {'ga': 'test-01', 'beta': 'localhost.localdomain'}
        user = request.user

        prd = request.POST.get('product', None)  # 选择的业务线
        pro = request.POST.get('project', None)  # 部署的项目
        # url = request.POST.get('url', None)
        # ver = request.POST.get('version', None)
        env = request.POST.get('env', None)  # 部署的环境
        ser = request.POST.get('op_interface', None)  # 部署的主机
        if prd is None:
            logger.error('部署失败，提交业务线表单不能为空')
            return redirect("error", next="code_deploy", msg="提交业务线表单不能为空，请填写完整")
        elif pro is None:
            logger.error('部署失败，提交项目表单不能为空')
            return redirect("error", next="code_deploy", msg="提交项目表单不能为空，请填写完整")
        elif ser is None:
            logger.error('部署失败，提交部署主机不能为空')
            return redirect("error", next="code_deploy", msg="提交部署主机不能为空，请填写完整")
        logging.debug('获取前端提交的上线项目: {}, 主机: {}; 环境:{} ; 操作人:{}'.format(pro, ser, env, user))

        obj = SaltApi()
        ret = obj.list_all_keys()

        # return JsonResponse({'project': pro, 'env': env, 'ret': ret, 'server': ser, 'test': prd + '.' + pro})
        #
        # if env == 'ga':
        #     obj.salt_state(ser, prd + '.' + pro)
        #     logger.debug('正在部署项目:{}'.format(pro))  # ps: salt 'ada-6' state.sls detalase.batch
        if env == 'ga':
            # jid = obj.async_remote_execution(ser, prd + '.' + pro)
            # logger.debug('正在异步部署项目:{}'.format(pro))
            try:
                jid = obj.async_remote_execution(ser, 'grains.item', ('os', 'id'))
                logger.debug('正在异步部署项目:{}'.format(jid))
            except KeyError as e:
                logger.error('部署失败, 详情: {}'.format(e.args))
                return redirect("error", next="code_deploy", msg="部署失败,{}".format(e.args))

        # 目前只是指定生产环境发布, 前端提交暂时写死了
        # elif env == 'beta':
        #     jid = sapi.async_remote_execution('tg', 'deploy.' + pro)

        # 获取 jid 的返回结果
        time.sleep(2)
        db = DB_Operate()
        sql = "select * from salt_returns where jid={}".format(str(jid))
        logger.debug('jid获取执行结果的sql: {}'.format(sql))
        try:
            ret = DB_Operate.select_table(self, RETURNS_MYSQL, sql)  # 通过jid获取执行结果
            context = {'ret': ret}
        except Exception as e:
            return redirect("error", next="code_deploy", msg="部署失败,{}".format(e.args))

        return render(request, 'code_update/deploy.html', context)

        def search(self, request):
            """这是一个知识点：
                自定义http_method_names： search
                需要在：
                1.http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'search', ]
                2.QueryDict(request.POST.get('project', None))
                """
            pass
