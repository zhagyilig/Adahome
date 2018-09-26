from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin  # 登陆验证
from django.http import JsonResponse
from core.tasks import show


# Create your views here.

class CodeDeployTemView(LoginRequiredMixin, TemplateView):
    pass
