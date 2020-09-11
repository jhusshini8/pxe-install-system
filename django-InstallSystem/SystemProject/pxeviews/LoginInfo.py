# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.http import JsonResponse
from SystemProject import models
import copy

def UserInfo(request):
    if (request.method == 'GET'):
        login_token = request.GET.get('token')
        authlogin = models.UserModle.objects.filter(username=login_token)
        print authlogin
        transferd_comment_list = []
        if authlogin:
            data_dic = {}
            for i in authlogin:
                data_dic["introduction"] = i.introduce
                data_dic['avatar'] = i.headimg
                data_dic["name"] = i.introduce
                data_dic["roles"] = ['admin']
                transferd_comment_list.append(data_dic.copy())
            result = dict()
            result["code"] = 20000
            result["data"] = data_dic
            return JsonResponse(result, safe=False)
        else:
            result = {}
            result["code"] = 50008
            result["message"] = "登录失败,用户名密码错误！"
            return JsonResponse(result, safe=False)