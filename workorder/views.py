from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin  # 登陆验证
from django.http import JsonResponse
from core.tasks import show


# Create your views here.

def celerytest(request):
    """180923 学习celery
    处理异步请求"""
    ret = {'status': 'ok'}
    # show() # 直接调用
    show.delay()  # 异步调用

    return JsonResponse(ret)
