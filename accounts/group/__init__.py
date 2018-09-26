# coding=utf-8
# author: zhangyiling


from django.contrib.auth.models import Group, User
from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin  # 登陆验证
from django.http import JsonResponse, HttpResponse, Http404


class GroupListView(LoginRequiredMixin, ListView):
    """展示用户组列表"""
    template_name = "accounts/grouplist.html"
    model = Group
    paginate_by = 10
    ordering = 'id'


class GroupCreateView(View):
    """展示用户组列表"""

    def post(self, request):
        """创建用户组"""
        result = {'status': 0}
        group_name = request.POST.get("name", "")  # ajax请求的带的参数: name
        if not group_name:
            result['status'] = 1
            result['errmsg'] = '用户组不能为空'  # 虽然前端已经验证了，但是可以用console改，所以后端也要做验证
            return JsonRespons(result, safe=True)
        try:
            g = Group(name=group_name)
            # g = Group()
            # g.name = group_name  # 创建组的两种方式
            g.save()
        except Exception as e:  # 如果组已经存在，则前端直接报 1062 异常
            result['status'] = 1
            result['errmsg'] = e.args
        return JsonResponse(result, safe=True)


class GroupUserView(LoginRequiredMixin, TemplateView):
    """展示指定用户组下成员列表"""
    template_name = 'accounts/group_userlist.html'
    per = 10  # 每页显示条目数

    def get_context_data(self, **kwargs):
        """
        获取模版传入的数据，这是固定的写法，需要记住
        这是内置的函数功能: 就是往模版里面传变量
        利用 Paginator, Page 进行分页
        """
        # 将指定用户组内的成员列表取出来，然后传给模版
        context = super(GroupUserView, self).get_context_data(**kwargs)
        gid = self.request.GET.get('gid', '')  # url 传来的gid 100

        try:
            group_obj = Group.objects.get(id=gid)
            # print(group_obj)   # dba, bi
            context['object_list'] = group_obj.user_set.all()  # 取出组中的用户
        except Group.DoesNotExist:
            raise Http404("用户组不存在")  # 抛出异常

        context['gid'] = gid  # 传到前端
        return context


class GroupMemListView(LoginRequiredMixin, TemplateView):
    """展示指定用户组下成员列表"""
    template_name = 'accounts/group_userlist.html'
    per = 2  # 每页显示条目数

    def get_context_data(self, **kwargs):
        """
        这是内置的函数功能: 就是往模版里面传变量
        利用 Paginator, Page 进行分页
        """
        context = super(GroupMemListView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1  # 默认起始的页码

        group_obj = Group.objects.get(id=gid)
        mem_list = Group.user_set.all()  # 获取所有的的组成员queryset

        paginator = Paginator(mem_list, self.per)  # 实例化一个paginator对象
        context['page_obj'] = paginator.page(page_num)  # 定义变量，返回一个page对象
        context['object_list'] = context['page_obj'].object_list
        return context
