# coding=utf-8
# auth: zhangyiling
# time: 2018/9/23 上午12:12
# description:

from django import forms
from monitor.models import Graph


class CreateGraphForm(forms.Form):
    """创建图形提交数据验证"""
    title = forms.CharField(required=True)
    subtitle = forms.CharField(required=False)  # 可以为空
    unit = forms.CharField(required=True)
    measurement = forms.CharField(required=True)
    auto_hostname = forms.CharField(required=False)
    field_expression = forms.CharField(required=False)
    tootip_formatter = forms.CharField(required=False)
    yaxis_formatter = forms.CharField(required=False)

    def isavailable(self, str):
        str = str.strip()
        if not str:
            return False
        return True

    def clean_title(self):
        """自定义验证的字段。必须是clean_ 开头"""
        title = self.cleaned_data['title']  # 值类型与字段定义的Field类型一致
        if not self.isavailable(title):
            raise forms.ValidationError('标题输入有误会, 请正确输入')
        return title

    def clean_unit(self):
        unit = self.cleaned_data['unit']
        if not self.isavailable(unit):
            raise forms.ValidationError('单位输入有误会, 请正确输入')
        return unit

    def clean_measurement(self):
        measurement = self.cleaned_data['measurement']
        if not self.isavailable(measurement):
            raise forms.ValidationError('表格输入有误会, 请正确输入')
        return measurement

    def clean_auto_hostname(self):
        auto_hostname = self.cleaned_data['auto_hostname']
        if auto_hostname == '1':
            return True
        return False

    def clean_yaxis_formatter(self):
        yaxis_formatter = self.cleaned_data['yaxis_formatter']
        return yaxis_formatter.strip()

    def clean_tootip_formatter(self):
        tootip_formatter = self.cleaned_data['tootip_formatter']
        return tootip_formatter.strip()
