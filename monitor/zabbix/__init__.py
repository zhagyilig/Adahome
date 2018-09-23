# coding=utf-8
# auth: zhangyiling
# time: 2018/9/8 下午10:06
# description:

from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import logging
from monitor.zabbix.client import cache_host

logger = logging.getLogger(__name__)


class ZabbixCacheHostView(LoginRequiredMixin, View):
    """同步zabbix缓存"""

    def get(self, request):
        logger.debug('开始同步zabbix缓存, 操作人:{}'.format(request.user.username))
        ret = {'status': 0}
        try:
            cache_host()
        except Exception as e:
            logger.error('同步zabbix缓存失败！！！')
            return JsonResponse({'status': 'error'})
        logger.debug('同步zabbix缓存完成')
        return JsonResponse(ret)
