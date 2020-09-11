# -*- coding:utf-8 -*-
from django.http import JsonResponse
from SystemProject import models
from datetime import datetime, timedelta
import xmlrpc.client
import os


class Pager(object):
    def __init__(self,current_page):
        self.current_page = int(current_page)
    @property
    def start(self):
        return (self.current_page-1) * 20
    @property
    def end(self):
        return self.current_page * 20

def FetchList(request):
    page = int(request.GET.get('page', 1))
    page_obj = Pager(page)
    global dataobj
    dataobj = ''

    if request.GET.get('type') and not request.GET.get('title'):
        type_style =  request.GET.get('type')
        dataobj = models.InstallRecord.objects.filter(version_name_id=type_style)[page_obj.start:page_obj.end]
    elif request.GET.get('title') and not request.GET.get('type'):
        title_style = request.GET.get('title')
        dataobj = models.InstallRecord.objects.filter(macaddr__contains=title_style)[page_obj.start:page_obj.end]
    elif request.GET.get('title') and  request.GET.get('type'):
        type_style = request.GET.get('type')
        title_style = request.GET.get('title')
        dataobj = models.InstallRecord.objects.filter(macaddr__contains=title_style,version_name_id=type_style)[page_obj.start:page_obj.end]
    else:
        dataobj = models.InstallRecord.objects.all()[page_obj.start:page_obj.end]

    systemobj = models.SystemType.objects.all()

    install_count = models.InstallRecord.objects.all().count()

    system_dic = {}
    transferd_comment_list = []
    transferd_system_list = []
    for i in systemobj:
        system_dic["key"] = i.id
        system_dic["display_name"] = i.record_list
        transferd_system_list.append(system_dic.copy())

    data_dic = {}
    for i in dataobj:
        data_dic["id"] = i.id
        now_time = i.installtime
        utc_time = now_time - timedelta(hours=8)
        utc_time = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        data_dic["timestamp"] = utc_time
        data_dic['title'] = i.macaddr
        data_dic["author"] = i.author
        data_dic["nodeip"] = i.ipaddr
        data_dic["versions"] = models.SystemType.objects.get(id=i.version_name_id).record_list
        data_dic["ipmiadd"] = i.ipmiaddr
        if int(i.installstatus) == 1:
            data_dic['status'] = "安装中"
        elif int(i.installstatus) == 2:
            data_dic['status'] = "成功"
        else:
            data_dic['status'] = "失败"
        data_dic["platforms"] = ["a-platform"]
        transferd_comment_list.append(data_dic.copy())
    result = dict()
    data_result = dict()
    data_result['calendarTypeOptions'] = transferd_system_list
    data_result["total"] = install_count
    data_result['items'] = transferd_comment_list
    result["code"] = 20000
    result["data"] = data_result
    return JsonResponse(result,safe=False)