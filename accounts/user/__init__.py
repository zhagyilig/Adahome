# coding=utf-8
# auth: zhangyiling

from django.views.generic import ListView  # 内置的列表(分页)功能
from django.views.generic import View
from django.contrib.auth.models import User, Group  # 要进行分页的数据库表（models）
from django.contrib.auth.mixins import LoginRequiredMixin  # 登陆验证
from django.http import HttpResponse, JsonResponse, QueryDict  # QueryDict：定义request.mode


class UserListView(LoginRequiredMixin, ListView):
    """权限列表页面添加权限按钮"""
    template_name = 'accounts/userlist.html'
    model = User
    paginate_by = 10  # 定义分页，没个page显示和数据条目
    ordering = 'id'  # 依据字段排序
    before_range_num = 4
    after_range_num = 5

    def get_queryset(self):
        """用户列表，但不展示超级管理员"""
        queryset = super(UserListView, self).get_queryset()  # queryset是一个集合，或者说是列表；
        # queryset = queryset.all().filter(username='zhangyiling') # 只显示 zhangyiling 这个账户
        # queryset = queryset.all().exclude(username='zhangyiling') # 不显示 zhangyiling 这个账户
        queryset = queryset.all().filter(is_superuser=False)

        keyword = self.request.GET.get('search_username', None)  # 关键字搜索
        if keyword:
            queryset = queryset.filter(username__icontains=keyword)  # 包含username的数据,i不区分大小写

        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

        # 当前页的前3条
        # current_page_index = context['page_obj'].number
        #
        # start = current_page_index - 3
        # end = current_page_index + 3
        #
        # if start <= 0:
        #     start =1
        #
        # if end > context['paginator'].num_pages:
        #     end = context['paginator'].num_pages
        #
        # context['page_range'] = range(start, end)
        # return context

        context['page_range'] = self.get_pagerange(context['page_obj'])

        # 处理搜索条件
        '''
        In [1]: from django.http import QueryDict
        
        In [2]: QueryDict('page=2&search_username=zhang-88')
        Out[2]: <QueryDict: {'page': ['2'], 'search_username': ['zhang-88']}>
        
        In [3]: q = QueryDict('page=2&search_username=zhang-88')
        
        In [4]: q.urlencode()
        Out[4]: 'page=2&search_username=zhang-88'
        
        In [5]: q.dict()
        Out[5]: {'page': '2', 'search_username': 'zhang-88'}
        
        In [6]: q.copy()
        Out[6]: <QueryDict: {'page': ['2'], 'search_username': ['zhang-88']}>
        
        In [7]: NewQ=q.copy()
        
        In [8]: NewQ
        Out[8]: <QueryDict: {'page': ['2'], 'search_username': ['zhang-88']}>
        '''

        search_data = self.request.GET.copy()
        try:
            search_data.pop('page')
        except:
            pass
        context.update(search_data.dict())

        context['search_data'] = '&' + search_data.urlencode()
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num

        if start <= 0:
            start = 1

        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end + 1)


class ModfiyUserStatusView(View):
    """修改用户状态"""

    def post(self, request):
        # print(request.POST)
        result = {"status": 0}
        uid = request.POST.get("uid", "")

        try:
            user_obj = User.objects.get(id=uid)
            user_obj.is_active = False if user_obj.is_active else True  # 改变用户状态，并保存
            user_obj.save()

        except User.DoesNotExist:  # 记录不存在的异常
            result["status"] = 1
            result["errmsg"] = "用不存在"
        return JsonResponse(result, safe=True)  # safe模式就是True


class ModfiyGroupStatusView(LoginRequiredMixin, View):
    """添加用户到指定组."""

    def get(self, request):
        """显示组名，但是如果用户已经添加到组，那该用户就不显示已经添加的组名."""
        # groups = Group.objects.all()
        '''
        print(groups)
        print(list(groups.values("id", "name")))
        
        <QuerySet [<Group: #5555%>, <Group: 88888>, <Group: devops>, <Group: kk>, <Group: op>, <Group: test>]>
        [{'id': 94, 'name': '#5555%'}, {'id': 95, 'name': '88888'}, {'id': 1, 'name': 'devops'}, {'id': 3, 'name': 'kk'}, {'id': 2, 'name': 'op'}, {'id': 96, 'name': 'test'}]
        '''

        print(request.GET)
        uid = request.GET.get('uid', '')
        group_objs = Group.objects.all()  # 这是数据库中全部的组

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list('id'))  # 排除已经添加的组名显示

        return JsonResponse(list(group_objs.values("id", "name")), safe=False)  # 传列表

    def put(self, request):
        """将用户添加到指定的组"""
        result = {"status": 0}
        data = QueryDict(request.body)  # django 中只封装了get和post，如果是需要put，就得使用这用这方式
        '''
        print(data)
        < QueryDict: {'uid': ['104'], 'gid': ['3']} >
        '''
        uid = data.get("uid", "")
        gid = data.get("gid", "")

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            result["status"] = 1
            result["errmsg"] = "用户不存在"
            return JsonResponse(result)

        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            result["status"] = 1
            result["errmsg"] = "用户组不存在"
            return JsonResponse(result)

        user_obj.groups.add(group_obj)  # 添加用户到组
        return JsonResponse(result, safe=True)

    def delete(self, request):
        """将用户从组中移除"""
        result = {"status": 0}
        data = QueryDict(request.body)  # django 中只封装了get和post，如果是需要put，就得使用这用这方式

        try:
            user_obj = User.objects.get(id=data.get('uid', ''))
        except User.DoesNotExist:
            result["status"] = 1
            result["errmsg"] = "用户不存在"
            return JsonResponse(result)

        try:
            group_obj = Group.objects.get(id=data.get('gid', ''))
        except Group.DoesNotExist:
            result["status"] = 1
            result["errmsg"] = "用户组不存在"
            return JsonResponse(result)

        user_obj.groups.remove(group_obj)  # 从组中移除用户

        # group_obj.objects.remove(user_obj) # 第二种方式： 从组中移除用户
        return JsonResponse(result, safe=True)


class GetUserView(LoginRequiredMixin, View):
    """业务线调用用户列表."""

    def get(self, request):
        users = User.objects.values('id', 'email', 'username')
        return JsonResponse(list(users), safe=False)
