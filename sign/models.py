from django.db import models
import datetime
# Create your models here.
from django.core.files.storage import FileSystemStorage

# fs = FileSystemStorage(location='/case')


class apis(models.Model):
    id = models.AutoField('ID', max_length=5, primary_key=True)
    path = models.URLField('接口路径', max_length=100, null=True)
    name = models.CharField('接口名称', max_length=200)
    method = models.CharField(max_length=10, choices=(('POST', 'POST'), ('GET', 'GET')), default='POST')    # choices=（value,display_name）
    content_type = models.CharField('数据传输方式', max_length=50, choices=(('JSON', 'JSON'), ('APPLICATION/X-WWW-FROM-URLENCODED', 'APPLICATION/X-WWW-FROM-URLENCODED')), default='JSON', null=True)
    belong_project = models.CharField('所属项目', max_length=20, choices=(('OC', 'OC'), ('PC', 'PC'), ('UC', 'UC'), ('SP', 'SP'), ('Odoo', 'Odoo')), default='OC')
    params = models.TextField('接口参数', max_length=5000)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    status = models.BooleanField('状态')

    class Meta:
        verbose_name = "接口列表"
        verbose_name_plural = "接口列表"

    def __str__(self):
        return self.name


class Case(models.Model):
    id = models.AutoField('ID', max_length=5, primary_key=True)
    name = models.CharField('用例名称', max_length=200)
    belong_project = models.CharField('所属项目', max_length=20, choices=(('OC', 'OC'), ('PC', 'PC'), ('UC', 'UC'), ('SP', 'SP'), ('Odoo', 'Odoo')), default='OC')
    description = models.CharField(max_length=200)
    file_name = models.FileField('文件名', null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    status = models.BooleanField('状态')


class Dependency(models.Model):
    id = models.AutoField('ID', max_length=5, primary_key=True)
    param = models.CharField('参数名', max_length=50, unique=True)
    value = models.CharField('参数值', max_length=500)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


class Schedule(models.Model):
    # 测试任务表
    id = models.AutoField('ID', max_length=5, primary_key=True)
    name = models.CharField('任务名', max_length=50, unique=True)
    env = models.CharField('环境', max_length=20)
    case_ids = models.CharField('用例ID', max_length=500)
    last_do_time = models.DateTimeField('上次执行时间', null=True)
    schedule_status = models.CharField('执行状态', max_length=10, default='未执行')
    do_times = models.IntegerField('执行次数', default=0)
    status = models.BooleanField('状态', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


class RunRecord(models.Model):
    # 执行记录表
    id = models.AutoField('ID', max_length=5, primary_key=True)
    schedule_ids = models.CharField('执行任务ID', max_length=500)
    total_count = models.IntegerField('用例总数', default=0)
    success_count = models.IntegerField('成功数', default=0)
    fail_count = models.IntegerField('失败数', default=0)
    spend_time = models.CharField('执行时间', max_length=50)
    schedule_result = models.CharField('执行结果', max_length=20, choices=(('Success', '成功'), ('Fail', '失败')))
    sequence = models.CharField('执行序列号', max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
