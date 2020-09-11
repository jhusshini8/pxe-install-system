# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.http import JsonResponse
from SystemProject import models


def UserLogout(request):
    if (request.method == 'POST'):
        print request.body

        data_dic = {}
        result = dict()
        result["code"] = 20000
        result["message"] = "退出系统"
        return JsonResponse(result, safe=False)
