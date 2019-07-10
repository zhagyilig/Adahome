# coding=utf-8
# auth: zhangyiling

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required  # 普通函数的登陆验证
from django.utils.decorators import method_decorator  # 类视图登陆验证
from django.contrib.auth.models import User  # 用户表
from django.views.generic import View  # 类视图
from django.views.generic import TemplateView  # 模版视图
from django.core.paginator import Paginator, Page  # 分页功能

'''
注意：需要加载模版数据(模版中有变量)就使用模版视图，直接返回模版就使用类视图
'''

'''
1.登陆系统功能
'''


# 使用普通函数实现登陆功能
def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    else:
        username = request.POST.get("username", "")  # 一定要添加默认 ""
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)  # 是否存在账户
        ret = {"status": 0, "errmsg": ""}
        if user:
            login(request, user)  # 用户是否为激活
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "账号或密码有误，请联系管理员"
        return JsonResponse(ret)


# 使用模版实现登陆功能
class LoginView(TemplateView):
    '''
    模版视图默认只定义了get方法；
    如果是需要 post 方法，那就得自己去实现, 其实就是：
    def post(self, request): 然后将上面("使用普通函数实现登陆功能")的代码copy
    '''
    template_name = "public/login.html"  # 默认就是get方法

    def post(self, request):
        '''自定义post方式.'''
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)  # 是否存在账户
        ret = {"status": 0, "errmsg": ""}
        if user:
            login(request, user)  # 用户是否为激活
            ret["next_url"] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret["status"] = 1
            ret["errmsg"] = "账号或密码有误,请联系管理员"
        return JsonResponse(ret, safe=True)  # 默认是True


'''
2.退出登陆功能
'''


# 使用普通函数实现注销功能
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))


# 使用类视图实现注销功能
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))


'''
3.获取用户列表
'''


def user_list_view(request):
    """普通函数实现."""
    user_queryset = User.objects.all()
    for user in user_queryset:
        # print(user.username, user.email)
        context = {'userllist': user_queryset}
    return render(request, "accounts/userlist.html", context)


class UserListView(View):
    # 类视图实现
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    @method_decorator(login_required)  # 类视图登陆验证
    def get(self, request, *args, **kwargs):
        user_queryset = User.objects.all()
        context = {'userllist': user_queryset}
        return render(request, "accounts/userlist.html", context)


'''
4.分页功能
'''


class UserTemView(TemplateView):
    # 学习模版视图
    template_name = 'accounts/userlist.html'
    per = 10  # 每页显示条目数

    @method_decorator(login_required)  # 模版view的验证，下面行也是的，都是做验证
    def get(self, request, *args, **kwargs):
        return super(UserTemView, self).get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     '''
    #     原始进行分页
    #     '''
    #     try:
    #         page = int(self.request.GET.get('num', 1))
    #     except:
    #         page = 1
    #     # end = per * page
    #     # start = end - per
    #     end = page * per
    #     start = per * (page - 1)
    #
    #     context = super(UserTemView, self).get_context_data()
    #     context["userllist"] = User.objects.all()[start:end]  # 变量传给模版； userlist:模版的变量名  all()数据
    #     return context

    def get_context_data(self, **kwargs):
        '''
        这是内置的函数功能: 就是往模版里面传变量
        利用 Paginator, Page 进行分页
        '''
        context = super(UserTemView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1  # 默认起始的页码

        user_list = User.objects.all()  # 获取所有的的用户queryset

        paginator = Paginator(user_list, self.per)  # 实例化一个paginator对象
        context['page_obj'] = paginator.page(page_num)  # 定义变量，返回一个page对象
        context['object_list'] = context['page_obj'].object_list
        return context