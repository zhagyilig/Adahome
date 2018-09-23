# coding=utf-8
# auth: zhangyiling

from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required  # 普通函数登陆验证
from django.utils.decorators import method_decorator  # 模版视图登陆验证
from django.views.generic import TemplateView  # 模版视图
from django.contrib.auth.mixins import LoginRequiredMixin  # 模版视图登陆验证
from django.utils.http import unquote_plus  # 反解析url # 对应加密url： servers.__init__.py


"""普通函数实现
@login_required
def index(request):
    return render(request, "dashboard/index.html")

模版视图实现
class IndexTemView(TemplateView):
    template_name = 'dashboard/index.html'

    @method_decorator(login_required)  # 模版视图的验证,下面两行也是的：其实就是在获取get之前添加验证
    def get(self, request, *args, **kwargs):
        return super(IndexTemView, self).get(request, *args, **kwargs)
"""

class IndexTemView(LoginRequiredMixin, TemplateView):  # 直接添加验证
    template_name = 'dashboard/index.html'


class SuccessTemView(LoginRequiredMixin, TemplateView):
    template_name = 'public/success.html'

    def get_context_data(self, **kwargs):
        '''
        这是内置的函数功能: 就是往模版里面传变量
        :param kwargs:
        :return:
        '''
        context = super(SuccessTemView, self).get_context_data(**kwargs)
        # print(self.kwargs)  # {'next': 'user_list'}
        # print(reverse(self.kwargs.get('next')))  # /accounts/user/list/

        success_url = self.kwargs.get('next', '')  # 成功页面之后要跳转的页面
        # next_url = '/'  # 180908 注释
        try:
            next_url = reverse(success_url)
        except:
            next_url = unquote_plus(success_url)

        context['next_url'] = next_url
        return context


class ErrorTemView(LoginRequiredMixin, TemplateView):
    template_name = 'public/error.html'

    def get_context_data(self, **kwargs):
        context = super(ErrorTemView, self).get_context_data(**kwargs)

        print(self.kwargs)

        error_url = self.kwargs.get('next', '')  # 成功页面之后要跳转的页面
        errormsg = self.kwargs.get('msg', '')  # 报错的内容
        # next_url = '/'
        try:
            next_url = reverse(error_url)
        except:
            next_url = unquote_plus(error_url)

        context['next_url'] = next_url
        context['errmsg'] = errormsg
        return context
