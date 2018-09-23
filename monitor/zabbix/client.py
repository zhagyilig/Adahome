# coding=utf-8
# auth: zhangyiling
# time: 2018/9/8 下午02:38
# description: 所有zabbix api操作在这里

from django.conf import settings  # 导入配置
from zabbix_client import ZabbixServerProxy
from monitor.models import ZabbixHost  # 缓存表
from resources.models import Server
import logging
import json

logger = logging.getLogger(name='django')


class Zabbix(object):
    """zabbix的一些操作"""

    def __init__(self):
        self.zb = ZabbixServerProxy(settings.ZABBIX_API)
        self.zb.user.login(user=settings.ZABBIX_USER, password=settings.ZABBIX_USERPASS)

    def get_host(self):
        """获取zabbix中的主机信息"""
        return self.zb.host.get(output=['host', 'hostid', ], selectInterfaces=["ip", ], )


def process_zb_hosts(zbhost):
    """处理主机ip地址"""
    logger.debug('处理已经从zabbix中获取的host信息')
    ret = []
    ip_list = []
    for host in zbhost:
        # host: {'hostid': '10084', 'host': '172.16.18.88', 'interfaces': [{'ip': '172.16.18.88'}]
        try:
            ip = host['interfaces'][0]['ip']
        except KeyError as e:
            logger.error('获取ip失败,{}, {}'.format(json.dumps(host), e.args))

        del host['interfaces']
        host['ip'] = ip
        ret.append(host)
        if ip in ip_list:
            logger.error('zabbix里多条相同ip地址[{}]'.format(ip))
        else:
            ip_list.append(ip)
    logger.debug('处理已经从zabbix中获取的host信息 完成')
    return ret


def cache_host():
    """获取zabbix中的主机和关联cmdb中的主机信息"""

    # 1. 取出所有的zabbix里的ip
    zbhosts = process_zb_hosts(Zabbix().get_host())
    # print('zhhosts: {}'.format(zbhosts))
    # ex: zhhosts: [{'hostid': '10084', 'host': '172.16.18.88', 'ip': '172.16.18.88'}]

    # 2. 关联cmdb中对应的记录
    for zbhost in zbhosts:

        try:
            # 拿zabbix中ip去Server查:
            print('zbhost:{}'.format(zbhost))
            # {'hostid': '10084', 'host': '172.16.18.88', 'ip': '172.16.18.88'}
            server_obj = Server.objects.get(inner_ip=zbhost['ip'])
            print('server_obj:{}'.format(server_obj))
            # zyl-node1 [172.16.18.88]
        except Server.DoesNotExist:
            logger.error('zabbix中的主机[{}], 在Ada resource.models.Server表中不存在'.format(zbhost['ip']))
        except Server.MultipleObjectsReturned:
            logger.error('zabbix中的主机[{}], 在Ada resource.models.Server表中存在多条记录'.format(zbhost['ip']))
        else:
            zbhost['server'] = server_obj
            print("host['server']: {}".format(zbhost['server']))
            zh = ZabbixHost(**zbhost)
            # zh.save()
            # logger.debug('zabbix中的主机[{}], 在Ada resource.models.Server表中保存成功'.format(zbhost['ip']))
            try:
                zh.save()
                logger.debug('zabbix中的主机[{}], 在Ada resource.models.Server表中保存成功'.format(zbhost['ip']))
            except Exception as e:
                logger.error('保存失败,详细信息: {}'.format(e.args))
    # 3. 告警(发邮件)


"""
Zabbix().get_host() ==> zbhost:
[{'hostid': '10084', 'host': '172.16.18.88', 'interfaces': [{'ip': '172.16.18.88'}]}, 
{'hostid': '10106', 'host': '172.16.18.66', 'interfaces': [{'ip': '172.16.18.66'}]}, 
{'hostid': '10107', 'host': '172.16.18.130', 'interfaces': [{'ip': '172.16.18.130'}]}]
"""
