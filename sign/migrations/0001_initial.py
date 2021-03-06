# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-07-10 17:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='apis',
            fields=[
                ('id', models.AutoField(max_length=5, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.URLField(max_length=100, null=True, verbose_name='接口路径')),
                ('name', models.CharField(max_length=200, verbose_name='接口名称')),
                ('method', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET')], default='POST', max_length=10)),
                ('content_type', models.CharField(choices=[('JSON', 'JSON'), ('APPLICATION/X-WWW-FROM-URLENCODED', 'APPLICATION/X-WWW-FROM-URLENCODED')], default='JSON', max_length=50, null=True, verbose_name='数据传输方式')),
                ('belong_project', models.CharField(choices=[('OC', 'OC'), ('PC', 'PC'), ('UC', 'UC'), ('SP', 'SP'), ('Odoo', 'Odoo')], default='OC', max_length=20, verbose_name='所属项目')),
                ('params', models.TextField(max_length=5000, verbose_name='接口参数')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2019, 7, 10, 17, 48, 28, 514243), verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.BooleanField(verbose_name='状态')),
            ],
            options={
                'verbose_name': '接口列表',
                'verbose_name_plural': '接口列表',
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(max_length=5, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='接口名称')),
                ('belong_project', models.CharField(choices=[('OC', 'OC'), ('PC', 'PC'), ('UC', 'UC'), ('SP', 'SP'), ('Odoo', 'Odoo')], default='OC', max_length=20, verbose_name='所属项目')),
                ('description', models.CharField(max_length=200)),
                ('file_name', models.FileField(null=True, upload_to='', verbose_name='文件名')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2019, 7, 10, 17, 48, 28, 515243), verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.BooleanField(verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(max_length=5, primary_key=True, serialize=False, verbose_name='ID')),
                ('param', models.CharField(max_length=50, unique=True, verbose_name='参数名')),
                ('value', models.CharField(max_length=500, verbose_name='参数值')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2019, 7, 10, 17, 48, 28, 516242), verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(max_length=5, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='任务名')),
                ('env', models.CharField(max_length=20, verbose_name='环境')),
                ('case_ids', models.CharField(max_length=500, verbose_name='用例ID')),
                ('schedule_time', models.DateTimeField(verbose_name='计划时间')),
                ('schedule_status', models.CharField(default='待执行', max_length=10, verbose_name='执行状态')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2019, 7, 10, 17, 48, 28, 518242), verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
    ]
