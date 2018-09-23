# coding=utf-8
# auth: zhangyiling


from django.conf.urls import include, url
from . import views


urlpatterns = [
    # url(r'^$', views.index, name='index'),  # 普通函数实现
    url(r'^$', views.IndexTemView.as_view(), name='index'),
    url(r'^success/(?P<next>[\s\S]*)/$', views.SuccessTemView.as_view(), name='success'), # 操作成功页面
    url(r'^error/(?P<next>[\s\S]*)/(?P<msg>[\s\S\\u4e00-\\u9fa5]*)/$', views.ErrorTemView.as_view(), name="error"), # 错误页面

]
