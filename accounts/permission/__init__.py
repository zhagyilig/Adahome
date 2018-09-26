# coding=utf-8
# author: zhangyiling


from django.contrib.auth.models import Permission, ContentType
from django.views.generic import ListView, TemplateView  # 视图
from django.contrib.auth.mixins import LoginRequiredMixin  # 权限验证
from django.http import HttpResponse
from django.shortcuts import redirect


class PermissionListView(LoginRequiredMixin, ListView):
    """展示权限列表"""
    model = Permission
    paginate_by = 10
    template_name = 'accounts/permission_list.html'
    ordering = 'id'


class PermissionAddTemView(LoginRequiredMixin, TemplateView):
    """权限列表页面添加权限按钮"""
    template_name = 'accounts/add_permission.html'

    def get_context_data(self, **kwargs):
        """加载模版数据"""
        context = super(PermissionAddTemView, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        return context

    def post(self, request):
        # print(request.POST)
        content_type_id = request.POST.get('content_type')
        codename = request.POST.get('codename')
        name = request.POST.get('name')

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            return redirect('error', next='permission_add', msg='模型不存在')
        if not codename or codename.find(' ') >= 0:  # .find(' ') >= 0 空格判断
            return redirect('error', next='permission_add', msg='codename不能为空或不能有空格')
        try:
            Permission.objects.create(content_type=content_type, codename=codename, name=name)
        except Exception as e:
            return redirect('error', next='permission_add', msg=e.args)
        return redirect('success', next='permission_list')  # 返回成功页面；next是success的关键参数名
