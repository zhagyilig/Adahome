# coding=utf-8
# author: zhangyiling


from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin  # 登陆验证
from django.shortcuts import redirect  # 页面跳转
from django.shortcuts import reverse  # 反转解析url的'name='
from django.http import HttpResponse
from resources.models import Idc
import json
from resources.forms import CreateIdcForm

'''
1. 添加idc, 使用模版视图
'''


class AddidcTemView(LoginRequiredMixin, TemplateView):
    template_name = 'resources/idc/add_idc.html'

    def post(self, request):
        '''
        获取添加idc表单提交的数据
        :param request:
        :return:
        '''
        # print(request.POST)  # 打印表单提交的数据

        # print(reverse('success', kwargs={'next': 'user_list'}))
        # 输出： /dashboard/success/user_list/

        # print(redirect('success', next='user_list'))
        # 输出： <HttpResponseRedirect status_code=302, "text/html; charset=utf-8", url="/dashboard/success/user_list/">

        # reverse
        # redirect: 两个的区别：reverse传入的是字典信息：kwargs；而redirect是arg，kwargs

        """ 更新使用django表单验证
        # 第一步： 获取表单数据
        name = request.POST.get('name', '')
        idc_name = request.POST.get('idc_name', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')

        # 第二步： 验证数据, 这里只是简单的校验
        error_msg = []
        if not name:
            error_msg.append('idc简称不能为空')

        if not idc_name:
            error_msg.append('idc_name不能为空')

        if error_msg:
            # print(error_msg)
            return redirect('error', next='add_idc', msg=json.dumps(error_msg, ensure_ascii=False))

        # 第三步： 实例化
        idc = Idc()
        idc.name = name
        idc.idc_name = idc_name
        idc.address = address
        idc.phone = phone
        idc.email = email
        idc.username = username

        try:
            idc.save()
        except Exception as e:
            return redirect('error', next='idc_list', msg=e.args)
        return redirect('success', next='idc_list')  # 返回成功页面；next是success的关键参数名
        # return redirect('error', next='user_list', msg='这是错误页面测试')# 返回错误页面；next/msg是error的关键参数名
        """

        # 使用django表单验证
        idcform = CreateIdcForm(request.POST)  # request.POST 表单提交的数据
        # print('idcform  %s' %idcform)

        if idcform.is_valid():  # 验证数据
            idc = Idc(**idcform.cleaned_data)  # cleaned_data 获取数据
            try:
                idc.save()
                return redirect('success', next='idc_list')
            except Exception as e:
                return redirect('error', next='idc_list', msg=e.args)

        else:
            # print(json.dumps(json.loads(idcform.errors.as_json()), ensure_ascii=False))
            # return HttpResponse('')
            error_msg = json.dumps(json.loads(idcform.errors.as_json()), ensure_ascii=False)
            return redirect('error', next='idc_list', msg=error_msg)


'''
2.idc 详细信息列表， 使用ListView
'''


class IdcListView(LoginRequiredMixin, ListView):
    template_name = 'resources/idc/idc_list.html'
    model = Idc
    paginate_by = 10  # 一个页面5个条目
    ordering = 'id'  # 列表按id排序
