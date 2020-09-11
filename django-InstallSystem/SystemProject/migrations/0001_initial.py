# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-08-21 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstallRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typename', models.IntegerField()),
                ('cobbler_name', models.CharField(max_length=32, null=True, verbose_name='cobbler\u540d')),
                ('ipmiaddr', models.CharField(max_length=32, verbose_name='ipmi\u5730\u5740')),
                ('ipmipass', models.CharField(max_length=32, verbose_name='ipmi\u5bc6\u7801')),
                ('ipaddr', models.CharField(max_length=32, verbose_name='ip\u5730\u5740')),
                ('gateaddr', models.CharField(max_length=32, null=True, verbose_name='\u7f51\u5173\u5730\u5740')),
                ('macaddr', models.CharField(max_length=32, verbose_name='mac\u5730\u5740')),
                ('installstatus', models.CharField(max_length=32, verbose_name='\u72b6\u6001')),
                ('installtime', models.DateTimeField(auto_now=True, verbose_name='\u5b89\u88c5\u65e5\u671f')),
                ('author', models.CharField(max_length=32, verbose_name='\u5b89\u88c5\u4eba')),
                ('remark_content', models.TextField(max_length=256, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'InstallRecord',
            },
        ),
        migrations.CreateModel(
            name='SystemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_list', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserModle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='\u7528\u6237\u540d')),
                ('passwd', models.CharField(max_length=32, verbose_name='\u5bc6\u7801')),
                ('introduce', models.CharField(max_length=64, verbose_name='\u7b80\u4ecb')),
                ('headimg', models.CharField(max_length=256, null=True, verbose_name='\u5934\u50cf')),
            ],
        ),
        migrations.AddField(
            model_name='installrecord',
            name='version_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='systemtype', to='SystemProject.SystemType'),
        ),
    ]