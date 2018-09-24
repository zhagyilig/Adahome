# coding=utf-8
# auth: zhangyiling
# time: 2018/9/24 下午11:33
# description: 工单系统

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class WorkOrder(models.Model):
    """工单系统"""
    ORDER_TYPE = (
        (0, '数据库'),
        (1, 'web服务'),
        (2, '计划任务'),
        (3, '配置文件'),
        (4, '其它'),
    )

    STATUS = (
        (0, '申请'),
        (1, '处理中'),
        (2, '完成'),
        (3, '失败'),
    )

    title = models.CharField(max_length=100, verbose_name='工单标题')
    type = models.IntegerField(choices=ORDER_TYPE, default=0, verbose_name='工单类型')
    order_contents = models.TextField(verbose_name='工单内容')
    applicant = models.ForeignKey(User, verbose_name='申请人', related_name='work_order_applicant')
    assign_to = models.ForeignKey(User, verbose_name='指派给谁')
    status = models.IntegerField(choices=STATUS, default=0, verbose_name='工单状态')
    result_desc = models.TextField(verbose_name='处理结果', blank=True, null=True)
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    complete_time = models.DateTimeField(auto_now_add=True, verbose_name='处理完成时间')

    def __str__(self):
        """django admin显示的字段"""
        return self.title

    class Meta:
        db_table = 'work_order'
        ordering=['-complete_time']
