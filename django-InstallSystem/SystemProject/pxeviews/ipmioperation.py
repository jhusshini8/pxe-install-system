# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.http import JsonResponse
from SystemProject import models
import xmlrpc.client


def getgateway(request):
    if (request.method == 'GET'):
        if request.GET.get('ipadd'):
            type_style = request.GET.get('ipadd')
            dataobj = models.InstallRecord.objects.filter(ipaddr=type_style)
            for i in dataobj:
                if int(i.installstatus) == 1:
                    result = {}
                    result["message"] = i.gateaddr
                    return JsonResponse(result, safe=False)

            result = {}
            result["message"] = "not find hostname"
            result["status"] = 0
            result["code"] = 20002
            return JsonResponse(result, safe=False)
        else:
                result = {}
                result["message"] = "not input ipaddr"
                result["status"] = 0
                result["code"] = 20003
                return JsonResponse(result, safe=False)