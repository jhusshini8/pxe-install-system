# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.http import JsonResponse
from SystemProject import models


def repassedit(request):
    if (request.method == 'POST'):
        print request.body
        postBody = request.body
        username = eval(postBody).get("username")
        passwd = eval(postBody).get("password")
        newpass1 = eval(postBody).get("newpassword1")
        newpass2 = eval(postBody).get("newpwd")
        if username and passwd:
            authpass = models.UserModle.objects.filter(username=username, passwd=passwd)
            if authpass:
                if newpass1 == newpass2:
                    models.UserModle.objects.filter(username=username).update(passwd=newpass2)
                    result = dict()
                    result["code"] = 20000
                    result["message"] = "修改成功"
                    return JsonResponse(result, safe=False)
                else:
                    result = dict()
                    result["code"] = 20002
                    result["message"] = "两次密码校验不一致"
                    return JsonResponse(result, safe=False)
            else:
                result = dict()
                result["code"] = 20002
                result["message"] = "旧密码错误"
                return JsonResponse(result, safe=False)