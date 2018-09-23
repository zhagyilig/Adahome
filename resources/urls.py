# coding=utf-8
# author: zhangyiling


from django.conf.urls import include, url
from . import views, idc, server, product

urlpatterns = [
    # 180819 资产管理
    url(r'^idc/', include([
        url(r'^add/$', idc.AddidcTemView.as_view(), name="add_idc"),  # 添加idc
        url(r'^list/$', idc.IdcListView.as_view(), name='idc_list'),  # idc列表
    ])),

    # 180902 上报资产
    url(r'^server/', include([
        url(r'^report/$', server.ServerInfoAutoReport, name='server_report'),  # 获取上报资产
        url(r'^list/$', server.ServerInfoListView.as_view(), name='server_list'),  # 资产列表
        url(r'^get/$', server.GetServerLiveView.as_view(), name='server_get'),  # 180906 获取服务器信息
        url(r'^refresh/$', server.RefreshLiveView.as_view(), name='server_refresh'),  # 刷新服务器信息
        url(r'^modify/', include([
            url(r'^product/$',  server.ServerModifyProductTemView.as_view(), name="server_modify_product"),  # 180907 修改主机的业务线信息
        ])),
    ])),

    # 180904 业务线
    url(r'^product/', include([
        url(r'^add/$', product.AddProductTemView.as_view(), name='product_add'),  # 添加业务线

        # 180905
        url('^ztree/$', product.ZnodeView.as_view(), name='product_ztree'),  # ztree显示业务线
        url(r'^get/$', product.ProductGetView.as_view(), name='product_get'),  # 获取业务线详情
        url(r'^manage/$', product.ProductManageTemView.as_view(), name='product_manage'),  # 业务线管理
    ])),
]
