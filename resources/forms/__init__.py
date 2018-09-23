# coding=utf-8
# author: zhangyiling

from django import forms
from resources.models import Idc, Product
from django.contrib.auth.models import User


class CreateIdcForm(forms.Form):
    '''
    验证创建idc表单提交的数据
    '''
    name = forms.CharField(required=True)
    idc_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True, error_messages={'invalid': '邮箱格式有误'})
    username = forms.CharField(required=True)

    def clean_name(self):
        '''
        自定义验证的字段, name。必须是clean_ 开头
        :return:
        '''
        name = self.cleaned_data.get('name')  # 获取name数据
        try:
            Idc.objects.get(name__exact=name)
            raise forms.ValidationError('idc名称已存在')
        except Idc.DoesNotExist:
            return name

    def clean(self):
        data = self.cleaned_data
        return data


class ProductForm(forms.Form):
    '''
    验证添加业务线表单提交的数据
    '''
    service_name = forms.CharField(required=True)
    module_letter = forms.CharField(required=True)
    op_interface = forms.MultipleChoiceField(
        choices=((u.email, u.username) for u in User.objects.filter(is_superuser=False)))
    dev_interface = forms.MultipleChoiceField(
        choices=((u.email, u.username) for u in User.objects.filter(is_superuser=False)))
    pid = forms.CharField(required=True)

    def clean_pid(self):
        '''
        自定义验证的字段，pid。必须是clean_ 开头
        :return:
        '''
        pid = self.cleaned_data['pid']
        if pid.isdigit():
            if int(pid) != 0:  # 0是一级业务线
                try:
                    p_obj = Product.objects.get(pk=pid)
                    if p_obj.pid != 0:
                        raise forms.ValidationError('请输入正确的一级业务线.')
                except Product.DoesNotExist:
                    raise forms.ValidationError('请输入正确的一级业务线..')
        else:
            raise forms.ValidationError('请输入正确的一级业务线...')
        return pid

    def clean_dev_interface(self):
        '''
        表单提交的是list，但是在db中是存的str，所以得转通过 ','.join() 转
        :return:
        '''
        dev_interface = self.cleaned_data['dev_interface']
        print(dev_interface)
        return ','.join(dev_interface)

    def clean_op_interface(self):
        '''
        表单提交的是list，但是在db中是存的str，所以得转通过 ','.join() 转
        :return:
        '''
        op_interface = self.cleaned_data['op_interface']
        print(op_interface)
        return ','.join(op_interface)
