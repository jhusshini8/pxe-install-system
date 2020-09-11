# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.http import JsonResponse
from SystemProject import models


def UserLogin(request):
    if (request.method == 'POST'):
        username = eval(request.body).get("username")
        passwd = eval(request.body).get("password")
        if username and passwd:
            authlogin = models.UserModle.objects.filter(username=username, passwd=passwd)
            if authlogin:
                data_dic = {}
                result = dict()
                data_dic["token"] = username
                result["code"] = 20000
                result["data"] = data_dic
                return JsonResponse(result, safe=False)

            else:
                result = {}
                result["status"] = 1
                result["code"] = 20002
                result["message"] = "登录失败,用户名密码错误！"
                return JsonResponse(result, safe=False)