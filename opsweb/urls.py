# coding=utf-8
# author: zhangyiling

"""opsweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView  # 用来进行跳转, 默认是永久重定向(301), 可以直接在urls.py中使用

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # django后台管理
    url(r'^$', RedirectView.as_view(url="/dashboard/")),  # 实现跳转的功能
    url(r'^dashboard/', include("dashboard.urls"), name="dashboard"),  # 控制面板
    url(r'^accounts/', include("accounts.urls"), name="accounts"),  # 权限管理
    url(r'^resources/', include("resources.urls"), name="resources"),  # 资产管理
    url(r'^monitor/', include("monitor.urls"), name='monitor'),  # 监控告警
    url(r'^code_update/', include("code_update.urls"), name='code_update'),  # 代码部署 # 180913
    url(r'^work_order/', include("workorder.urls"), name='workorder'),  # 工单系统 # 180924

]
