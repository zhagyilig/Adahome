# coding=utf-8
# auth: zhangyiling
# time: 2018/9/24 上午09:12
# description: 重建用户表

"""
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserMessage(models.Model):
    '''发送消息'''
    user = models.IntegerField(default=0, verbose_name='修改用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = 'user_messgae'
        verbose_name_plural = verbose_name


class UserProfile(AbstractUser):
    '''重写用户表'''
    name = models.CharField('中文名', max_length=30)
    phone = models.CharField('手机', max_length=11, null=True, blank=True)
    wechat = models.CharField('微信', max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'userprofile'

    def __str__(self):
        return self.name

    def unread_message(self):
        unread_messages = UserMessage.objects.filter(user=self.id, has_read=False)
        return unread_messages
"""
