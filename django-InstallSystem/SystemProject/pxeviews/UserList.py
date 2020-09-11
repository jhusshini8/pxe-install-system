# -*- coding:utf-8 -*-
from django.http import JsonResponse
from SystemProject import models

def UserListPage(request):
    if (request.method == 'GET'):
        dataobj = models.InstallRecord.objects.all()
        data_dic = {}
        transferd_comment_list = []
        for i in dataobj:
            data_dic["name"] = i.author
            transferd_comment_list.append(data_dic.copy())
        result = dict()
        data_result = dict()
        data_result['items'] = transferd_comment_list
        result["code"] = 20000
        result["data"] = data_result
        return JsonResponse(result, safe=False)

def UserListPageAll(request):
    if (request.method == 'GET'):
        dataobj = models.InstallRecord.objects.all()
        install_count = models.InstallRecord.objects.all().count()
        data_dic = {}
        transferd_comment_list = []
        for i in dataobj:
            data_dic["id"] = i.id
            if int(i.installstatus) == 1:
                data_dic['status'] = "安装中"
            elif int(i.installstatus) == 2:
                data_dic['status'] = "成功"
            elif int(i.installstatus) == 3:
                data_dic['status'] = "删除"
            else:
                data_dic['status'] = "失败"
            data_dic["name"] = i.author
            data_dic["installsystem"] = models.SystemType.objects.get(id=i.version_name_id).record_list
            transferd_comment_list.append(data_dic.copy())
        result = dict()
        data_result = dict()
        data_result["total"] = install_count
        data_result['items'] = transferd_comment_list
        result["code"] = 20000
        result["data"] = data_result
        return JsonResponse(result, safe=False)