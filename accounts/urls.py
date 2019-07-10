# conding:utf-8
# auth: zhangyiling


from django.conf.urls import url, include
from . import views, user, group, permission

urlpatterns = [
    # 登陆和注销功能
    # url(r'^login/$', views.login_view, name='user_login'),  # 普通函数
    url(r'^login/$', views.LoginView.as_view(), name='user_login'),  # 模版视图

    # url(r'^logout/$', views.logout_view, name="user_logout"),
    url(r'^logout/$', views.LogoutView.as_view(), name="user_logout"),

    # 视图和分页的学习
    # url(r'^user/list/$', views.user_list_view, name="user_list"),  # 普通函数
    # url(r'^user/list/$', views.UserListView.as_view(), name="user_list"), # 类视图

    # url(r'^user/list/$', views.UserTemView.as_view(), name="user_list"), # 模版视图，并使用函数分页功能
    # url(r'^user/list/$', user.UserListView.as_view(), name="user_list"),  # 使用django内置listview进行分页

    # url(r'^use/(20)/$', views.user_detail, name="user_detail"),  # 位置参数
    # url(r'^use/([0-9]+)/(?P<id>[0-9]{,4})/$', views.user_detail, name="user_detail"),  # 关键字参数

    # 180812 用户管理
    url(r'^user/', include([
        url(r'^list/$', user.UserListView.as_view(), name="user_list"),  # 类视图，用户列表
        url(r'^modify/', include([
            url(r'^status/$', user.ModfiyUserStatusView.as_view(), name="user_modify_status"),  # 改变用户状态
            url(r'^group/$', user.ModfiyGroupStatusView.as_view(), name="user_modify_group"),  # 添加用户到组
        ])),
        url(r'^get/$', user.GetUserView.as_view(), name='user_list_get'),  # 180905 业务线调用用户列表
    ])),

    # 180812 用户组管理
    url(r'^group/', include([
        url(r'^list/$', group.GroupListView.as_view(), name="group_list"),  # 组列表
        url(r'^create/$', group.GroupCreateView.as_view(), name="group_create"),  # 创建组模态窗
        url(r'^members_list/$', group.GroupUserView.as_view(), name="group_members_list"),  # 组成员列表
        url(r'^members_page/$', group.GroupMemListView.as_view(), name="group_page_list"),  # 搜索分页
    ])),

    # 180821 权限列表
    url(r'^permission/', include([
        url(r'^list/$', permission.PermissionListView.as_view(), name="permission_list"),  # 权限列表
        url(r'^add/$', permission.PermissionAddTemView.as_view(), name="permission_add"),  # 权限列表
    ])),
]
