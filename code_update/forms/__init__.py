# # coding=utf-8
# # auth: zhangyiling
# # time: 2018/9/18 上午2:49
# # description:
#
#
# from django import forms
# from resources.models import Server
# from django.contrib.auth.models import User
#
#
# class CodeDeploy(forms.Form):
#     '''
#     验证发布代码提交的数据
#     '''
#
#     op_interface = forms.MultipleChoiceField(
#         choices=((u.email, u.username) for u in User.objects.filter(is_superuser=False)))
#     dev_interface = forms.MultipleChoiceField(
#         choices=((u.email, u.username) for u in User.objects.filter(is_superuser=False)))
#     pid = forms.CharField(required=True)
#
#     def clean_pid(self):
#         '''
#         自定义验证的字段，pid。必须是clean_ 开头
#         :return:
#         '''
#         pid = self.cleaned_data['pid']
#         if pid.isdigit():
#             if int(pid) != 0:  # 0是一级业务线
#                 try:
#                     p_obj = Product.objects.get(pk=pid)
#                     if p_obj.pid != 0:
#                         raise forms.ValidationError('请输入正确的一级业务线.')
#                 except Product.DoesNotExist:
#                     raise forms.ValidationError('请输入正确的一级业务线..')
#         else:
#             raise forms.ValidationError('请输入正确的一级业务线...')
#         return pid
#
#     def clean_dev_interface(self):
#         '''
#         表单提交的是list，但是在db中是存的str，所以得转通过 ','.join() 转
#         :return:
#         '''
#         dev_interface = self.cleaned_data['dev_interface']
#         print(dev_interface)
#         return ','.join(dev_interface)
#
#     def clean_op_interface(self):
#         '''
#         表单提交的是list，但是在db中是存的str，所以得转通过 ','.join() 转
#         :return:
#         '''
#         op_interface = self.cleaned_data['op_interface']
#         print(op_interface)
#         return ','.join(op_interface)
