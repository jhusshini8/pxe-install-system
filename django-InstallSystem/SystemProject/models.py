# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime

# Create your models here.

class SystemType(models.Model):
    GENDER_CHOICES = ()
    record_list = models.CharField(max_length=32,choices=GENDER_CHOICES,unique=True)

class UserModle(models.Model):
    username = models.CharField('用户名', max_length=32,unique=True)
    passwd = models.CharField('密码', max_length=32)
    introduce = models.CharField('简介', max_length=64)
    headimg = models.CharField('头像', max_length=256,null=True)

class InstallRecord(models.Model):
    typename = models.IntegerField()
    cobbler_name = models.CharField('cobbler名', max_length=32,null=True)
    ipmiaddr = models.CharField('ipmi地址', max_length=32)
    ipmipass = models.CharField('ipmi密码', max_length=32)
    ipaddr = models.CharField('ip地址', max_length=32)
    gateaddr = models.CharField('网关地址', max_length=32,null=True)
    macaddr = models.CharField('mac地址', max_length=32)
    installstatus = models.CharField('状态', max_length=32)
    installtime = models.DateTimeField('安装日期', auto_now=True, blank=True)
    author = models.CharField('安装人', max_length=32)
    version_name = models.ForeignKey('SystemType',related_name='systemtype')
    remark_content = models.TextField('备注', max_length=256,null=True)

    class Meta:
        db_table = 'InstallRecord'
        ordering = ('-id',)


# class ns_record(models.Model):
#     zone_ns = models.CharField('ns记录', max_length=32,unique=True)

# class roomtoany(models.Model):
#     zone_hearder = models.CharField('主机头',max_length=32,blank=True,null=True)
#     zone_in = models.CharField(default='IN',max_length=32,blank=True)
#     zone_ip = models.CharField('解析记录',max_length=256)
#     edit_time = models.DateTimeField('修改日期', auto_now=True,blank=True)
#     mx_level = models.IntegerField(blank=True,null=True)
#     zone_ttl = models.IntegerField(default=600,blank=True,null=True)
#     associated_type = models.ForeignKey('record_type',related_name='type_list')
#     host_domain = models.ForeignKey('domain',related_name='domain_list')
#     zone_ns = models.ForeignKey('ns_record', related_name='ns_list')
#     room = models.CharField('IDC',default='ANY',max_length=8)
#
# class dnsdbuser(models.Model):
#     chinaname = models.CharField('中文名',max_length=12)
#     username = models.CharField('登录用户名',max_length=12,unique=True)
#     passwd = models.CharField('密码',max_length=32)
#     portrait = models.CharField('头像',max_length=256)
#
# class access_count(models.Model):
#     idc = models.CharField('机房',max_length=24)
#     accesslist = models.CharField('七天数据',max_length=256)
#     datainfo = models.CharField('日期',max_length=256,null=True)