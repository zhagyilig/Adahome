# coding=utf-8
# auth: zhangyiling
# time: 2018/9/23 上午5:59
# description: 异步处理请求; 所有的耗时处理在这里

import time
from celery import task
import logging

logger = logging.getLogger(__name__)


@task
def show():
    """这个函数就是celery的一个任务
    在code_update.view中调用
    """
    logging.debug('hello....')
    time.sleep(5)
    logging.debug('world...')
