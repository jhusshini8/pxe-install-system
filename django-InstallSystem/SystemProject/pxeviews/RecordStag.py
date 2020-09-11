# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.http import JsonResponse
from SystemProject import models
import xmlrpc.client
import global_settings

def RecordStag_sucess(request):
    if (request.method == 'POST'):
        postBody = request.body
        nodename = eval(postBody).get("nodename")
        stagstatus = int(eval(postBody).get("suctag"))
        models.InstallRecord.objects.filter(cobbler_name=nodename).update(installstatus=stagstatus)
        remote_server = xmlrpc.client.Server(global_settings.server)
        token = remote_server.login(global_settings.user, global_settings.password)
        try:
            remote_server.remove_system(nodename, token)
            remote_server.sync(token)
        except:
            result = {}
            result["message"] = "not find hostname"
            result["status"] = 0
            result["code"] = 20002
            return JsonResponse(result, safe=False)

        result = {}
        result["message"] = "sucess"
        result["status"] = 0
        result["code"] = 20000
        return JsonResponse(result, safe=False)

def RecordStag_install(request):
    if (request.method == 'POST'):
        postBody = request.body
        print postBody
        stagid = eval(postBody).get("id")
        stagstatus = int(eval(postBody).get("tempstat"))
        alrelystag = int(models.InstallRecord.objects.get(id=stagid).installstatus)
        print alrelystag,stagstatus
        if alrelystag == stagstatus:
            result = {}
            result["message"] = "已经是安装失败状态"
            result["status"] = 1
            result["code"] = 20001
            return JsonResponse(result, safe=False)

        elif alrelystag == 2:
            result = {}
            result["message"] = "成功状态不可标记为失败"
            result["status"] = 1
            result["code"] = 20001
            return JsonResponse(result, safe=False)

        else:
            models.InstallRecord.objects.filter(id=stagid).update(installstatus=stagstatus)
            remote_server = xmlrpc.client.Server(global_settings.server)
            token = remote_server.login(global_settings.user, global_settings.password)

            node_hostname = str(models.InstallRecord.objects.get(id=stagid).cobbler_name)
            try:
                remote_server.remove_system(node_hostname, token)
                remote_server.sync(token)
            except:
                pass
            # 1 安装 2 成功 3失败 4错误
            # for i in remote_server.get_systems():
            #     try:
            #         node_hostname = i['hostname']
            #         if models.InstallRecord.objects.get(id=stagid).ipaddr:
            #             installstat = int(models.InstallRecord.objects.get(id=stagid).installstatus)
            #             # print installstat,'sadasd'
            #             # print node_hostname
            #             if installstat > 1:
            #                 remote_server.remove_system(node_hostname, token)
            #                 remote_server.sync(token)
            #     except:
            #         pass
            result = {}
            result["message"] = "标记状态成功"
            result["status"] = 0
            result["code"] = 20000
            return JsonResponse(result, safe=False)