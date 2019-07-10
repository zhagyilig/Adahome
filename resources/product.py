# coding=utf-8
# auth: zhangyiling

from django.views.generic import ListView, View, TemplateView  # 需要返回json数据就用View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import ProductForm  # 表单验证
from resources.models import Product, Idc
import json

'''
1. 业务线
'''


class AddProductTemView(LoginRequiredMixin, TemplateView):
    template_name = 'resources/server/add_product.html'

    def get_context_data(self, **kwargs):
        context = super(AddProductTemView, self).get_context_data(**kwargs)
        context['userlist'] = User.objects.filter(is_superuser=False)  # 过滤超级管理员
        context['products'] = Product.objects.filter(pid__exact=0)  # 精确匹配

        return context

    def post(self, request):
        '''
        获取添加业务线表单的数据
        :param request:
        :return:
        '''
        print(request.POST)
        product_form = ProductForm(request.POST)  # 验证提交的数据
        # 测试:
        # product_form.is_valid()
        # return JsonResponse({'status': 'success'})

        if product_form.is_valid():  # 验证数据
            pro = Product(**product_form.cleaned_data)  # cleaned_data 获取数据
            try:
                pro.save()
                return redirect('success', next='product_manage')
            except Exception as e:
                return redirect('error', next='product_manage', msg=e.args)

        else:
            error_msg = json.dumps(json.loads(product_form.errors.as_json()), ensure_ascii=False)
            return redirect('error', next='product_manage', msg=error_msg)


'''
2. 业务线管理
'''








class ProductManageTemView(LoginRequiredMixin, TemplateView):
    template_name = 'resources/server/product_manage.html'

    def get_context_data(self, **kwargs):
        context = super(ProductManageTemView, self).get_context_data(**kwargs)
        context['ztree'] = Ztree().get() # 前端var zNodes = {{ ztree|safe }};
        return context


'''
3. ztree显示业务线树状
'''


class ZnodeView(LoginRequiredMixin, View):
    def get(self, request):
        ztree = Ztree()
        znode = ztree.get()
        print('zonde: ', znode)
        return JsonResponse(znode, safe=False)


class Ztree(object):
    def __init__(self):
        self.data = self.get_product()

    def get_product(self):
        # 获取Product表的数据
        return Product.objects.all()

    def get(self, idc=False):
        '''
        处理一级业务线
        :return:
        '''
        ret = []
        for p in self.data.filter(pid=0):
            print('p :', p)
            node = {
                'name': p.service_name,
                'id': p.id,
                'pid': p.pid,
                'children': self.get_children(p.id),  # 二级业务线的pid是一级业务线的id
                'isParent': 'true', # 这里是js中的true
            }
            ret.append(node)
        if idc:
            return self.get_idc(ret)
        else:
            return ret

    def get_children(self, id):
        '''
        处理二级业务线
        :param id: 一级业务线的id，就是二级业务线的pid
        :return:
        '''
        ret = []
        for p in self.data.filter(pid=id):  # 二级业务线的pid是一级业务线的id
            print('get_children: ', p)
            node = {
                'name': p.service_name,
                'id': p.id,
                'pid': p.pid,
            }
            ret.append(node)
        return ret

    def get_idc(self, nodes):
        '''
        获取idc，作为ztree的顶级
        :param nodes:
        :return:
        '''
        ret = []
        for i in Idc.objects.all():
            node = {
                'name': i.idc_name,
                'children': nodes,  # nodes 就是上面一级业务线
                'isParent': 'true', # 这里是json中的true
            }
            ret.append(node)
        return ret


'''
4.  业务线详情
'''

class ProductGetView(LoginRequiredMixin, View):
    def get(self, request):
        ret = {"status": 0}

        # 1 根据product id, 取指定的一条记录
        p_id = self.request.GET.get("id", None)
        p_pid = self.request.GET.get("pid", None)


        if p_id:
            ret["data"] = self.get_obj_dict(p_id)

        # 2 根据product pid, 取出多条记录
        if p_pid:
            ret["data"] = self.get_products(p_pid)

        # 3 不传任何值，所出所有记录
        return JsonResponse(ret)

    def get_obj_dict(self, p_id):
        try:
            obj = Product.objects.get(pk=p_id)
            ret = obj.__dict__  # 我们是需要字典数据结构
            ret.pop("_state")  # 取出的字典数据，有多余的字段，见下面的测试
            return ret
        except Product.DoesNotExist:
            return {}

    def get_products(self, pid):
        return list(Product.objects.filter(pid=pid).values())

        '''
        测试：
            In [8]: p = Product.objects.get(pk=1)
            
            In [9]: p
            Out[9]: <Product: 物流系统>
            
            In [10]: p.__dict__
            Out[10]:
            {'_state': <django.db.models.base.ModelState at 0x7f15855d17f0>,
             'id': 1,
             'service_name': '物流系统',
             'module_letter': 'ALS',
             'op_interface': 'zhang-1@ezbuy.com,zhang-3@ezbuy.com',
             'dev_interface': 'zyl@qq.com,zhang-8@ezbuy.com',
             'pid': 0}
            
            In [11]: d = p.__dict__
            
            In [12]: d
            Out[12]:
            {'_state': <django.db.models.base.ModelState at 0x7f15855d17f0>,
             'id': 1,
             'service_name': '物流系统',
             'module_letter': 'ALS',
             'op_interface': 'zhang-1@ezbuy.com,zhang-3@ezbuy.com',
             'dev_interface': 'zyl@qq.com,zhang-8@ezbuy.com',
             'pid': 0}
            
            In [13]: d.pop('_state')
            Out[13]: <django.db.models.base.ModelState at 0x7f15855d17f0>
            
            In [14]: d
            Out[14]:
            {'id': 1,
             'service_name': '物流系统',
             'module_letter': 'ALS',
             'op_interface': 'zhang-1@ezbuy.com,zhang-3@ezbuy.com',
             'dev_interface': 'zyl@qq.com,zhang-8@ezbuy.com',
             'pid': 0}
        '''