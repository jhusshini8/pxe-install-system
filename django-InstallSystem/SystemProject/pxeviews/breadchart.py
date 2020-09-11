# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.http import JsonResponse
from SystemProject import models
import time, datetime

def GetBreadChart(request):
    systemlist = models.SystemType.objects.all()
    transferd_system_list = []
    transferd_comment_list = []
    for i in systemlist:
        transferd_system_list.append(i.record_list)
        system_id = i.id
        succe_count = models.InstallRecord.objects.filter(version_name_id=system_id).count()
        transferd_comment_list.append(succe_count)

    new_dic = dict(zip(transferd_system_list,transferd_comment_list))
    dict_list = []
    new_list = []
    dict_new = {}
    for k in new_dic.keys():
        dict_temp = k, new_dic[k]
        dict_list = list(dict_temp)
        dict_new["name"] = dict_list[0]  # 添加
        dict_new["value"] = dict_list[1]
        new_list.append(dict_new)
        dict_new = {}

    result = dict()
    data_result = dict()
    result["temp"] = new_list
    result["code"] = 20000
    result["data"] = transferd_system_list
    return JsonResponse(result, safe=False)