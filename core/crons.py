# coding=utf-8
# auth: zhangyiling
# time: 2018/9/23 上午10:10
# description:  系统所有的定时任务在这里

import logging

logger = logging.getLogger(__name__)


def test_django_crontab():
    """学习django定时任务"""
    logger.debug("执行指定定时任务:test_django_crontab ")
    print('django_crontab test....')
