# coding=utf-8
# auth: zhangyiling

import datetime
import logging
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlquote_plus  # url编码
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers  # 数据转成json
from django.shortcuts import get_object_or_404  # 如果不能获取表中的数据，则抛出404
from django.utils.http import urlquote_plus  # 加密url
from resources.models import Server, Product  # 自定义的models
from core.saltapi import SaltApi  # 刷新服务信息需要salt api

logger = logging.getLogger(__name__)


@csrf_exempt  # 强制取消csrf验证
def ServerInfoAutoReport(request):
    """获取采集脚本提交的数据，使用普通函数实现"""
    if request.method == "POST":
        data = request.POST.dict()
        data['check_update_time'] = datetime.datetime.now()
        try:
            Server.objects.get(uuid__exact=data['uuid'])
            Server.objects.filter(uuid=data['uuid']).update(**data)  # 一条记录全部更新

            """
            # 指定字段更新
            s.hostname = data['hostname']
            s.check_update_time = datetime.now()
            s.save(update_fields=['hostname'])
            """
        except Server.DoesNotExist:
            s = Server(**data)
            s.save()
        return HttpResponse('')


class ServerInfoListView(LoginRequiredMixin, ListView):
    """资产列表，使用类视图实现"""
    model = Server
    template_name = 'resources/server/server_list.html'
    paginate_by = 8  # 定义分页，没个page显示和数据条目
    ordering = 'id'  # 依据字段排序
    before_range_num = 4
    after_range_num = 5

    def get_queryset(self):
        """关键字搜索"""
        queryset = super(ServerInfoListView, self).get_queryset()
        keyword = self.request.GET.get('search_hostname', '')  # 关键字搜索
        if keyword:
            queryset = queryset.filter(hostname__icontains=keyword)  # 包含hostname的数据,i不区分大小写
        return queryset

    def get_product(self):
        """获取业务线名"""
        ret = {}
        for obj in Product.objects.all():
            ret[obj.id] = obj.service_name
        print(ret)
        return ret

    # 下面两个函数是定义分页功能
    def get_context_data(self, **kwargs):
        context = super(ServerInfoListView, self).get_context_data(**kwargs)
        context['page_range'] = self.get_pagerange(context['page_obj'])
        context['product'] = self.get_product()
        search_data = self.request.GET.copy()
        try:
            search_data.pop('page')
        except:
            pass
        context.update(search_data.dict())

        # context['search_data'] = '&' + search_data.urlencode() # 之前server_list.html需要的 &
        # 去掉url的 &
        search_url_str = search_data.urlencode()
        if search_url_str:
            context['search_data'] = '&' + search_url_str
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num

        if start <= 0:
            start = 1

        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end + 1)


class GetServerLiveView(LoginRequiredMixin, View):
    """根据二级业务线的id，取出服务器信息"""

    def get(self, request):
        server_purpose = request.GET.get("server_purpose", None)

        # 获取某台机器的所有信息
        # 待开发.....

        # 获取某个业务线下的所有机器列表
        if server_purpose:
            queryset = Server.objects.filter(server_purpose=server_purpose).values("id", "hostname", "inner_ip")
            return JsonResponse(list(queryset), safe=False)

        return JsonResponse([], safe=False)


class ServerModifyProductTemView(LoginRequiredMixin, TemplateView):
    """修改服务器信息"""
    template_name = 'resources/server/server_modify_product.html'

    def get_context_data(self, **kwargs):
        """加载模版数据"""
        context = super(ServerModifyProductTemView, self).get_context_data(**kwargs)

        server_id = self.request.GET.get('id', None)
        # print('server_id： ' + server_id)

        context['server'] = get_object_or_404(Server, pk=server_id)
        context['products'] = Product.objects.filter(pid=0)
        return context

    def get(self, request, *args, **kwargs):
        """修改业务线点击提交之后的跳转页面 测试"""
        print(request.GET)  # <QueryDict: {'id': ['76'], 'next': ['/resources/server/list/?page=10']}>

        next_url = (request.GET.get('next', None))
        print(next_url)
        print(reverse('success', kwargs={'next': 'server_list'}))
        print(reverse('success', kwargs={'next': urlquote_plus(next_url)}))

        '''
        <QueryDict: {'id': ['47'], 'next': ['/resources/server/list/?page=6']}>
        /resources/server/list/?page=6
        /dashboard/success/server_list/
        /dashboard/success/%252Fresources%252Fserver%252Flist%252F%253Fpage%253D6/
        如果要是实现跳转： 将server_list 改成 /resources/server/list/?page=6    
        '''
        return super(ServerModifyProductTemView, self).get(request, *args, **kwargs)

    def post(self, request):
        # 获取修改主机业务线的数据，并修改主机业务线
        # 知识点： get_object_or_404 和 升级表中的部分字段数据
        # 下面涉及到了两张表:  Server, Product

        # print(request.GET)  # <QueryDict: {'id': ['3'], 'next': ['/resources/server/list/']}>
        next_url = request.GET.get('next', None) if request.GET.get('next', None) else 'server_list'

        server_id = request.POST.get("id", None)
        service_id = request.POST.get("service_id", None)
        server_purpose = request.POST.get("server_purpose", None)

        # print(server_id, service_id, service_purpose)
        try:
            server_obj = Server.objects.get(pk=server_id)
        except Server.DoesNotExist:
            return redirect("error", next="server_list", msg="服务器不存在")

        try:
            product_service_id = Product.objects.get(pk=service_id)

        except Product.DoesNotExist:
            return redirect("error", next="server_list", msg="一级业务线不存在")

        try:
            product_server_purpose = Product.objects.get(pk=server_purpose)
        except Product.DoesNotExist:
            return redirect("error", next="server_list", msg="二级业务线不存在")

        if product_server_purpose.pid != product_service_id.id:  # 二级业务线.pid == 一级业务线的.id
            raise Http404
        server_obj.service_id = product_service_id.id
        server_obj.server_purpose = product_server_purpose.id
        server_obj.save(update_fields=["service_id", "server_purpose"])

        # return  redirect('success', next='server_list')
        return redirect(reverse('success', kwargs={'next': urlquote_plus(next_url)}))


class RefreshLiveView(LoginRequiredMixin, ListView):
    """刷新服务器信息"""

    def __init__(self):
        self.obj = SaltApi()  # 实例化

    def get(self, request):
        """获取salt-minion系统信息"""
        os_info = {
            'client': 'local',
            'fun': 'grains.item',
            'tgt': '*',
            'arg': ('osfinger', 'fqdn', 'host', 'ipv4', 'mem_total', 'num_cpus', 'uuid'),
            'kwargs': {},
            'expr_form': 'glob',
            'timeout': 300,
        }

        # 所有的minion key
        all_key = self.obj.list_all_keys()  # tuple: (['study-zyl-node5'], [])
        logger.debug('所有的minion列表: {}'.format(all_key))

        # minion的系统详细信息
        for host in all_key:
            logger.debug('要循环的minion: {}'.format(host))
            info = self.obj.run(os_info)
            try:
                minion = host[0]
            except IndexError as e:
                logger.error('all_key有None, 具体的异常: {}'.format(e.args))
                continue

            # 获取eth0网卡地址(ipv4):
            ipv4 = self.obj.remote_execution('*', 'grains.item', ('ip4_interfaces'))[minion]['ip4_interfaces']['eth0']
            print('ipv4: {}'.format(ipv4))

            # 数据库主机信息过滤条件
            uu_id = info[minion]['uuid']
            # print('uuid:', uu_id)

            # 要入库的系统数据
            data = {}
            data['hostname'] = info[minion]['host']
            data['inner_ip'] = ipv4[0]
            data['server_cpu'] = info[minion]['num_cpus']
            data['server_mem'] = float('%.2f' % (info[minion]['mem_total'] / 1024))
            data['uuid'] = info[minion]['uuid']
            data['os'] = info[minion]['osfinger']
            data['check_update_time'] = datetime.datetime.now()

            # salt minion在线依据,minion的运行状态
            status = self.obj.salt_alive(minion, 'glob')  # True/False
            data['status'] = status[minion]
            # print('data:', data)

            try:
                logger.debug('开始主机[{}]入库操作, 操作人: {}......'.format(uu_id, request.user))

                # 如果有主机uuid信息, 则更新主机信息
                Server.objects.get(uuid__exact=uu_id)
                Server.objects.filter(uuid=uu_id).update(**data)  # 一条记录全部更新
                logger.debug('更新主机完成: {}'.format(uu_id))
            except Server.DoesNotExist:
                # 如果没有过滤到uuid信息，则是新主机入库
                logger.debug('新入库主机: {}'.format(uu_id))
                s = Server(**data)
                try:
                    s.save()
                except Exception as e:
                    logger.error('主机入库失败, 报错信息: {}'.format(e.args))
                    return redirect('error', next='server_list', msg=e.args)

        return redirect('success', next='server_list')
