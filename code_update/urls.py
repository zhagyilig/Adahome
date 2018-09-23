# coding=utf-8
# author: zhangyiling


from django.conf.urls import include, url
from . import deploy
from . import views

urlpatterns = [
    url(r'^deploy/$', deploy.CodeDeployTemView.as_view(), name="code_deploy"),  # 代码部署
    # url(r'^restart/$', deploy.CodeDeployTemView.as_view(), name="code_restart"),  # 代码回滚
    # url(r'^recover/$', deploy.CodeDeployTemView.as_view(), name="code_recover"),  # 代码重启
    url(r'^stucelery/$', views.celerytest, name="celerytest"),  # 代码重启
]
