# coding=utf-8
# auth: zhangyiling
# time: 2018/9/13 下午8:33
# description: 代码发布，回退相关的代码


import time
import logging
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin  # 登陆验证
from django.http import JsonResponse, QueryDict
from code_update.models import ServicesName
from resources.models import Server
from core.saltapi import SaltApi

logger = logging.getLogger(__name__)


class CodeDeployTemView(LoginRequiredMixin, TemplateView):
    """代码发布"""
    template_name = 'code_update/deploy.html'

    # 需要自定义method的方式
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'search', ]

    def get_context_data(self, **kwargs):
        """加载所有的项目及服务列表"""
        context = super(CodeDeployTemView, self).get_context_data(**kwargs)
        context['servernames'] = ServicesName.objects.all()  # 项目名列表
        context['serverlists'] = Server.objects.all()  # 服务器列表
        logging.debug('加载所有的项目成功: {}'.format(context))
        return context

    def post(self, request):
        """获取前端提交的项目，并发布项目"""
        ret = ''
        host = {'ga': 'test-01', 'beta': 'localhost.localdomain'}
        user = request.user

        pro = request.POST.get('project', None)
        # url = request.POST.get('url', None)
        # ver = request.POST.get('version', None)
        env = request.POST.get('env', None)
        deploy_ser = request.POST.get('selected', None)
        logging.debug('获取前端提交的上线项目: {}, 主机: {}; 环境:{} ;操作人:{}'.format(pro, env, deploy_ser, user))
        print(pro, env, deploy_ser)

        obj = SaltApi()
        ret = obj.list_all_keys()
        print('sapi: {}'.format(obj))
        return JsonResponse({'project': pro, 'env': env, 'ret': ret, 'server': deploy_ser})

        # if env == 'beta':
        #     jid = sapi.async_remote_execution('beta', 'deploy.' + pro)
        # elif env == 'ga':
        #     jid = sapi.async_remote_execution('tg', 'deploy.' + pro)
        # else:
        #     jid = sapi.async_remote_execution('beta', 'deploy.' + pro)

        # time.sleep(8)
        # db = db_operate()
        # sql = 'select returns from salt_returns where jid=%s'
        # ret = db.select_table(settings.RETURNS_MYSQL, sql, str(jid))  # 通过jid获取执行结果
        # return render_to_response('code_deploy.html',
        #                           {'ret': ret}, context_instance=RequestContext(request))

        def search(self, request):
            """这是一个知识点：
                自定义http_method_names： search
                需要在：
                1.http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'search', ]
                2.QueryDict(request.POST.get('project', None))
                """
            pass
