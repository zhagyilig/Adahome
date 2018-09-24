# coding=utf-8
# auth: zhangyiling
# time: 2018/9/24 下午11:42
# description: 工单系统


from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^apply/$', views.CodeDeployTemView.as_view(), name="work_order_apply"),
    # url(r'^list/$', views.CodeDeployTemView.as_view(), name="work_order_list"),
    # url(r'^detail/$', views.CodeDeployTemView.as_view(), name="work_order_detail"),
    # url(r'^history/$', views.CodeDeployTemView.as_view(), name="work_order_history"),
]
