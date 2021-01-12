# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.http import JsonResponse
from SystemProject import models
import time, datetime

def GetLine(request):
    if (request.method == 'GET'):
        def get_week_day(date):
            week_day_dict = {
                0: '星期一',
                1: '星期二',
                2: '星期三',
                3: '星期四',
                4: '星期五',
                5: '星期六',
                6: '星期天',
            }
            day = date.weekday()
            return week_day_dict[day]

    def getdate(beforeOfDay):
        today = datetime.datetime.now()
        # 计算偏移量
        offset = datetime.timedelta(days=-beforeOfDay)
        # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y-%m-%d')
        return re_date

    # 获取前一周的所有日期(weeks=1)，获取前N周的所有日期(weeks=N)
    def getBeforeWeekDays(weeks=1):
        global faild_list,succ_list
        faild_list = []
        succ_list = []
        # 0,1,2,3,4,5,6,分别对应周一到周日
        week = datetime.datetime.now().weekday()
        days_list = []
        start = 7 * weeks + week
        end = week
        for index in range(start - 1, end - 1, -1):
            day = getdate(index)
            faild_stg = models.InstallRecord.objects.filter(installtime__startswith=day,installstatus=5).count()
            succ_stg = models.InstallRecord.objects.filter(installtime__startswith=day, installstatus=2).count()
            faild_list.append(faild_stg)
            succ_list.append(succ_stg)
    getBeforeWeekDays(1)

    week_date = [1,2,3,4,5,6,7]
    week_day = []
    today = datetime.date.today()
    for i in week_date[::-1]:
        yesterday = today - datetime.timedelta(days=i)
        thistime = yesterday.isoweekday()
        if thistime == 1:
            a = "周一"
        elif thistime == 2:
            a = "周二"
        elif thistime == 3:
            a = "周三"
        elif thistime == 4:
            a = "周四"
        elif thistime == 5:
            a = "周五"
        elif thistime == 6:
            a = "周六"
        elif thistime == 7:
            a = "周日"
        week_day.append(a)
    user_count = int(models.UserModle.objects.all().count())
    install_count = int(models.InstallRecord.objects.all().count())
    succe_count = models.InstallRecord.objects.filter(installstatus=2).count()
    faild_count = models.InstallRecord.objects.filter(installstatus=5).count()
    result = dict()
    data_result = dict()
    result["code"] = 20000
    result["usercount"] = user_count
    result["installcount"] = install_count
    result["succount"] = succe_count
    result["faildcount"] = faild_count
    data_result['actualData'] = succ_list
    data_result['expectedData'] = faild_list
    result["newVisitis"] = data_result
    result["data"] = week_day
    return JsonResponse(result, safe=False)
