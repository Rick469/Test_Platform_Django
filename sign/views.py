# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import apis, Case, Dependency, Schedule, RunRecord
import requests, xlrd,xlwt, json, os
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib import messages
from sign.test_tools import TestTools
import datetime
import decimal
from sign.config.path import api_case_file_dir
from sign.API_Test.create_scripts import Create


def index(request):
    """index首页"""
    return render(request, 'base.html') #返回获取的数据行


def paginate(objs, page=1):
    """重新封装分页器"""
    paginator = Paginator(objs, 20)     # 分页器对象,每页大小为20
    total_pages = paginator.num_pages       # 总页数
    list= paginator.page(page).object_list   # 当前请求页case列表
    r = {'current_page': page, 'total_pages': total_pages, 'list': list}
    return r


def api_list(request):
    """接口列表页"""
    flag = request.GET.get('flag', '')
    message = request.GET.get('message', '')
    api_obj = apis.objects.all().order_by('-id')  # 通过objects这个模型管理器的all()获得apis表中所有数据行，相当于SQL中的SELECT * FROM

    page = request.GET.get('page', 1)       # 取请求的页码，默认值为首页1
    result = paginate(api_obj, page)

    if flag and message:
        result.update({'flag': flag, 'message': message})
        return render(request, 'api_list.html', result)
    else:
        return render(request, 'api_list.html', result)


def api_list_filter(request):
    """接口列表筛选器"""
    print(request.GET.copy())
    api_address = request.GET.get('search_address', '')
    api_name = request.GET.get('search_name', '')
    api_belong_project = request.GET.get('search_belong_project', '')
    origin_data = {'api_address': api_address, 'api_name': api_name, 'api_belong_project': api_belong_project}

    api_list = apis.objects.filter(path__contains=api_address, name__contains=api_name, belong_project__contains=api_belong_project).order_by('-id')
    print(api_list)
    page = request.GET.get('page', 1)       # 取请求的页码，默认值为首页1
    result = paginate(api_list, page)
    result.update({'origin_data': origin_data})
    return render(request, 'api_list.html', result)     # 返回获取的数据行


def api_detail(request):
    """接口详情页"""
    id = request.GET.get('id')
    api = apis.objects.get(id=id)   # 获取单个对象，通过id值获取数据行
    return render(request, 'api_detail.html', {'api': api})


def api_add(request):
    return render(request, 'api_add.html')


def api_add_save(request):
    try:
        print(request.POST.copy())
        name = request.POST.get('api_name')
        belong_project = request.POST.get('api_belong_project')
        address = request.POST.get('api_address')
        method = request.POST.get('api_method')
        content_type = request.POST.get('api_content_type', '')
        params = request.POST.get('body').strip()

        if method == 'POST':
            if content_type == 'JSON':  # JSON格式body需要先JSON化再存入数据库
                params = json.dumps(eval(params))   # 去除params空格和换行符，并转为Json格式
        ob = apis.objects.create(name=name, belong_project=belong_project, path=address, method=method, content_type=content_type, params=params, status=True)
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/api/list/?flag=fail&message=添加失败： internal error')
    else:
        return HttpResponseRedirect('/api/list/?flag=success&message=添加成功')


def api_edit(request):
    operation = request.GET.get('operation')
    id = request.GET.get('id')
    api = apis.objects.get(id=id)

    if operation == 'query':    # 编辑-详情页
        return render(request, 'api_edit.html', {'api': api})

    elif operation == 'save':   # 保存更改
        print(request.POST.copy())
        name = request.POST.get('api_name')
        belong_project = request.POST.get('api_belong_project')
        address = request.POST.get('api_address')
        method = request.POST.get('api_method')
        content_type = request.POST.get('api_content_type', '')
        params = request.POST.get('body').strip()

        if method == 'POST':
            if content_type == 'JSON':  # JSON格式body需要先JSON化再存入数据库
                params = json.dumps(eval(params))   # 去除params空格和换行符，并转为Json格式
        try:
            # api = apis.objects.filter(id=id)
            # api.update(name=name, belong_project=belong_project, address=address, method=method, content_type=content_type, params=body)
            api.name = name
            api.belong_project = belong_project
            api.path = address
            api.method = method
            if method == 'POST':
                api.content_type = content_type
            elif method == 'GET':
                api.content_type = ''
            api.params = params
            api.save()
        except Exception as e:
            print(e)
            return HttpResponseRedirect('/api/list/?flag=fail&message=更新失败： internal error')
        else:
            return HttpResponseRedirect('/api/list/?flag=success&message=更新成功')
    elif operation == 'delete':
        try:
            api.delete()
        except Exception as e:
            print(e)
            return HttpResponseRedirect('/api/list/?flag=fail&message=删除失败： internal error')
        else:
            return HttpResponseRedirect('/api/list/?flag=success&message=删除成功')


def case_list(request):
    flag = request.GET.get('flag', '')
    message = request.GET.get('message', '')

    cases_obj = Case.objects.all().order_by('-id')  # 通过objects这个模型管理器的all()获得apis表中所有数据行，相当于SQL中的SELECT * FROM

    page = request.GET.get('page', 1)  # 取请求的页码，默认值为首页1
    result = paginate(cases_obj, page)

    if flag and message:
        result.update({'flag': flag, 'message': message})
        return render(request, 'case_list.html', result)
    else:
        return render(request, 'case_list.html', result)


# def case_list_paginator(request):
#     # json_request = json.loads(request)
#     # page = json_request.get('page', 1)
#     # page_size = json_request.get('page_size', 1)
#     page = request.GET.get('page', 1)
#     page_size = request.GET.get('page_size', 1)
#     cases = Case.objects.all().order_by('-id')
#     paginator = Paginator(cases, page_size)
#     total_pages = paginator.num_pages
#     case_list = paginator.page(page).object_list

    # 返回Json格式数据实现Ajax分页
    # response_case = []
    # for case in case_list:
    #     response_case.append({'case_id': case.id, 'case_name': case.name, 'case_desc': case.description, 'case_create_time': case.create_time.strftime("%Y-%m-%d %H:%M:%S"), 'case_status': case.status, 'file_name': str(case.file_name)})
    # response = {'page_count': page_count, 'response_case': response_case}
    # print(response)
    # return HttpResponse(json.dumps(response))
    # return render(request, 'case_list.html', {'cases': case_list, 'total_pages': total_pages, 'current_page': page})


def case_list_filter(request):
    """用例筛选器"""
    print(request.GET.copy())
    case_desc = request.GET.get('search_desc', '')
    case_name = request.GET.get('search_name', '')
    origin_data = {'case_desc': case_desc, 'case_name': case_name}
    case_list = Case.objects.filter(description__contains=case_desc, name__contains=case_name).order_by('-id')
    print(case_list)
    page = request.GET.get('page', 1)       # 取请求的页码，默认值为首页1
    result = paginate(case_list, page)
    result.update({'origin_data': origin_data})
    return render(request, 'case_list.html', result)     # 返回获取的数据行


def case_add(request):
    return render(request, 'case_add.html')


def case_add_save(request):
    case_name = request.POST.get('case_name')
    case_desc = request.POST.get('case_desc')
    case_file = request.FILES.get("case_file")
    case_belong_project = request.POST.get('case_belong_project')
    print(request.POST.copy())
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + case_file.name
    f = open(api_case_file_dir+file_name, 'wb+')
    for chunk in case_file.chunks():
        f.write(chunk)
    f.close()
    try:
        ob = Case.objects.create(name=case_name,belong_project=case_belong_project, description=case_desc, file_name=file_name, status=True)
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/case/list/?flag=fail&message=添加失败： internal error')
    else:
        return HttpResponseRedirect('/case/list/?flag=success&message=添加成功')


def case_edit(request):
    operation = request.GET.get('operation')
    id = request.GET.get('id')
    case = Case.objects.get(id=id)

    if operation == 'query':    # 编辑-详情页
        return render(request, 'case_edit.html', {'case': case})

    elif operation == 'save':   # 保存更改
        case_name = request.POST.get('case_name')
        case_desc = request.POST.get('case_desc')
        case_file = request.FILES.get('case_file')
        case_belong_project = request.POST.get('case_belong_project')
        print(request.POST.copy(), '\n', case_file)

        if case_file:       # 有文件上传才存储文件
            file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + case_file.name
            f = open(api_case_file_dir + file_name, 'wb+')
            for chunk in case_file.chunks():
                f.write(chunk)
            f.close()
        try:
            case.name = case_name
            case.description = case_desc
            case.belong_project = case_belong_project
            if case_file:
                case.file_name = file_name      # 有新的文件上传才更新file_name
            case.save()
        except Exception as e:
            print(e)
            return HttpResponseRedirect('/case/list/?flag=fail&message=更新失败： internal error')
        else:
            return HttpResponseRedirect('/case/list/?flag=success&message=更新成功')
    elif operation == 'delete':
        try:
            case.delete()
        except Exception as e:
            print(e)
            return HttpResponseRedirect('/case/list/?flag=fail&message=删除失败： internal error')
        else:
            return HttpResponseRedirect('/case/list/?flag=success&message=删除成功')


def schedule_list(request):

    # 若是HttpResponseRedirect到此页面则有flag和message，相应显示出来；直接访问没有该值
    flag = request.GET.get('flag', '')
    message = request.GET.get('message', '')

    schedule_obj = Schedule.objects.all().order_by('-id')  # 通过objects这个模型管理器的all()获得apis表中所有数据行，相当于SQL中的SELECT * FROM

    page = request.GET.get('page', 1)  # 取请求的页码，默认值为首页1
    result = paginate(schedule_obj, page)
    if flag and message:
        result.update({'flag': flag, 'message': message})
        return render(request, 'schedule_list.html', result)
    else:
        return render(request, 'schedule_list.html', result)


def schedule_list_filter(request):
    env = request.GET.get('search_env', '')
    name = request.GET.get('search_name', '')
    schedule_status = request.GET.get('search_schedule_status', '')
    origin_data = {'env': env, 'name': name, 'schedule_status': schedule_status}

    schedule_list = Schedule.objects.filter(env__contains=env, name__contains=name, schedule_status__contains=schedule_status).order_by('-id')
    page = request.GET.get('page', 1)       # 取请求的页码，默认值为首页1
    result = paginate(schedule_list, page)
    result.update({'origin_data': origin_data})
    return render(request, 'schedule_list.html', result)     # 返回获取的数据行


def schedule_add(request):
    schedule_name = request.POST.get('schedule_name')
    schedule_env = request.POST.get('schedule_env')
    schedule_case_ids = request.POST.get('case_ids')
    try:
        ob = Schedule.objects.create(name=schedule_name, env=schedule_env, case_ids=schedule_case_ids)
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/case/list/?flag=fail&message=添加失败： internal error')
    else:
        return HttpResponseRedirect('/case/list/?flag=success&message=添加成功')


def schedule_delete(request):
    id = request.GET.get('id')
    schedule = Schedule.objects.get(id=id)
    try:
        schedule.delete()
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/schedule/list/?flag=fail&message=删除失败： internal error')
    else:
        return HttpResponseRedirect('/schedule/list/?flag=success&message=删除成功')


def deependency_list(request):
    # 若是HttpResponseRedirect到此页面则有flag和message，相应显示出来；直接访问没有该值
    flag = request.GET.get('flag', '')
    message = request.GET.get('message', '')

    dependency_obj = Dependency.objects.all().order_by('-id')   # 通过objects这个模型管理器的all()获得apis表中所有数据行，相当于SQL中的SELECT * FROM

    page = request.GET.get('page', 1)  # 取请求的页码，默认值为首页1
    result = paginate(dependency_obj, page)
    if flag and message:
        result.update({'flag': flag, 'message': message})
        return render(request, 'dependency_list.html', result)
    else:
        return render(request, 'dependency_list.html', result)


def deependency_list_filter(request):
    param = request.GET.get('search_param', '')
    value = request.GET.get('search_value', '')
    origin_data = {'param': param, 'value': value}

    dependency_list = Dependency.objects.filter(param__contains=param, value__contains=value).order_by('-id')
    page = request.GET.get('page', 1)       # 取请求的页码，默认值为首页1
    result = paginate(dependency_list, page)
    result.update({'origin_data': origin_data})
    return render(request, 'dependency_list.html', result)     # 返回获取的数据行


def run_test(request):
    """接口详情-单个接口调用"""
    print(request.POST.copy())
    id = request.POST.get('id')  # 获取接口ID
    api = apis.objects.get(id=id)    # 获取单个对象，通过id值获取数据行
    method = api.method
    url = 'http://'+api.belong_project+'-staging.ehsy.com'+api.path
    test_data = request.POST.copy()         # copy request请求对象（因为原request请求对象不可更改）
    test_data.pop('id')  # 只留下输入框填写的数据，去掉带过来的id值
    test_data = test_data.get('data')
    test_data = eval(test_data)
    print(test_data, type(test_data))

    if method == 'POST':
        if api.content_type == 'APPLICATION/X-WWW-FROM-URLENCODED':
            r = requests.post(url, data=test_data)
        if api.content_type == 'JSON':
            r = requests.post(url, json=test_data)
    if method == 'GET':
        r = requests.get(url, params=test_data)
    print(r.text)
    return HttpResponse(r.text)


def upload_case(request):
    """批量测试HTML对应view函数"""
    return render(request, 'upload_case.html',)


def schedule_run(request):
    ids = request.POST.get('ids', '').split(',')
    if not ids:
        result = {'mark': '1', 'message': '没有Schedule ID'}
    else:
        sequence = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        schedule_objs = Schedule.objects.filter(id__in=ids)

        case_done = []  # 已生成scripts的case_id列表
        # 循环所有执行任务对象
        for schedule in schedule_objs:
            # 更新任务表"上次执行时间"和"执行次数字段"
            schedule.last_do_time = datetime.datetime.now()
            schedule.do_times = schedule.do_times + 1
            schedule.schedule_status = '已执行'
            schedule.save()

            # 获取schedule的env(接口测试执行环境）值
            env = schedule.env

            # 取出所有case_id
            case_ids = schedule.case_ids.split(',')

            # 遍历用例ID生成脚本（每个用例生成一个脚本）
            for id in case_ids:

                # 该case在其他schedule中已经生成过脚本则无需重复生成
                if id in case_done:
                    continue

                # 未生成脚步的需要生成,同时添加id到已生成列表case_done
                else:
                    file_name = str(Case.objects.get(id=id).file_name)
                    create = Create(file_name, sequence)
                    script_name = create.make_test_script(env)

                    # 添加case_id到已生成列表case_done
                    case_done.append(id)
        print('--------------已生成脚本case_id:----------------', '\n', case_done)

        import unittest
        from BeautifulReport import BeautifulReport
        pattern = 'test_'+sequence+'*.py'
        suit = unittest.defaultTestLoader.discover(
            r'C:\Users\rick_zhang\Desktop\Test_Platform\sign/API_Test/api_test_case/', pattern=pattern)
        result = BeautifulReport(suit).report(filename=sequence+'Report.html', description='API-AutoTest-Report',
                                               log_path=r'C:\Users\rick_zhang\Desktop\Test_Platform\sign//static/api_test_file/api_test_report/')
        r = {'message': '执行完毕，请查看测试报告'}

        # 创建执行记录
        schedule_ids = ','.join(list(case_ids))
        schedule_result = 'Success'
        if result['testFail'] != 0:
            schedule_result = 'Fail'
        totalTime = result['totalTime']
        total_count = result['testAll']
        success_count = result['testPass']
        fail_count = result['testFail']
        record = RunRecord.objects.create(schedule_ids=schedule_ids, total_count= total_count, success_count=success_count, fail_count=fail_count, spend_time=totalTime, schedule_result=schedule_result, sequence=sequence)
    return HttpResponse(json.dumps(r))


def api_report(request):
    flag = request.GET.get('flag', '')
    message = request.GET.get('message', '')

    record_obj = RunRecord.objects.all().order_by('-id')  # 通过objects这个模型管理器的all()获得apis表中所有数据行，相当于SQL中的SELECT * FROM

    page = request.GET.get('page', 1)  # 取请求的页码，默认值为首页1
    result = paginate(record_obj, page)

    if flag and message:
        result.update({'flag': flag, 'message': message})
        return render(request, 'api_report.html', result)
    else:
        return render(request, 'api_report.html', result)


# def batch_test(request):
#     """批量测试按钮触发的动作函数"""
#     if request.method == "POST":    # 请求方法为POST时，进行处理
#         myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
#         if not myFile:
#             messages.error(request, "no files for upload!")
#             return render(request, 'upload_case.html')
#         destination = open(os.path.join("./case", myFile.name), 'wb+')    # 打开特定的文件进行二进制的写操作
#         for chunk in myFile.chunks():      # 分块写入文件
#             destination.write(chunk)
#         flag = True  # 标志是否有用例失败
#         p = 0  # 成功的case数量
#         f = 0  # 失败的case数量
#         rows_fail = []  # excel中失败行
#         fail_reason = []    # 失败原因
#         file = './case/'+myFile.name    # 文件路径
#         data = xlrd.open_workbook(file)
#         table = data.sheet_by_index(0)      # 读取excel sheet页
#         rows = table.nrows      # 获取当前sheet页数据行数
#         # 接口测试报告
#         report = xlwt.Workbook()
#         report_table = report.add_sheet('接口测试结果')
#         styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour gray50')
#         font_color = xlwt.easyxf('font: colour_index red')
#         report_table.write(0,0,'序号', styleBlueBkg)
#         report_table.write(0, 1, '接口名称', styleBlueBkg)
#         report_table.write(0, 2, '接口URL', styleBlueBkg)
#         report_table.write(0, 3, 'message', styleBlueBkg)
#         report_table.write(0, 4, '执行结果', styleBlueBkg)
#         report_table.write(0, 5, '执行时间(s)', styleBlueBkg)
#         first_col = report_table.col(1)    # 获取列
#         second_col = report_table.col(2)
#         third_col = report_table.col(3)
#         four_col = report_table.col(5)
#         first_col.width = 256*10     # 设置列宽
#         second_col.width = 256*50
#         third_col.width = 256*10
#         four_col.width = 256*15
#         report.save('./sign/static/file/report.xls')
#         for row in range(1, rows):
#             excel_data = table.row_values(row)  # 获取当前行的数据（列表对象）
#             url = excel_data[2]
#             method = excel_data[3].lower()
#             params = excel_data[4]
#             message_assert = excel_data[5].strip()      # strip去掉首尾空格
#             start_time = datetime.datetime.now()
#             if method == 'post':
#                 params = eval(params)    # excel表中的字符串转换为字典
#                 r = requests.post(url, data=params)
#             if method == 'get':
#                 params = eval(params)
#                 r = requests.get(url, params=params)
#             end_time = datetime.datetime.now()
#             run_time = str(end_time - start_time)[6:10]
#             if method != 'post' and method != 'get':
#                 messages.error(request, 'Method填写错误')
#                 return render(request, 'upload_case.html')
#             result = r.json()
#             print(result['message'])
#             # 接口测试报告写入
#             report_table.write(row,0,row)
#             report_table.write(row,1,excel_data[1])
#             report_table.write(row, 2, url)
#             report_table.write(row, 3, result['message'])
#             if result['message'] == message_assert:     # 断言
#                 p += 1
#                 report_table.write(row, 4, 'pass')
#             else:
#                 f += 1
#                 rows_fail.append(str(row + 1))
#                 fail_reason.append(result['message'])
#                 report_table.write(row, 4, 'fail', font_color)
#             report_table.write(row, 5, run_time)
#             report.save('./sign/static/file/report.xls')
#         tips = {'成功': p, '失败': f, '失败行数': (','.join(rows_fail) or '无'), '失败原因': (','.join(fail_reason) or '无')}
#         if f != 0:
#             flag = False
#         if flag:    # 根据flag判断message是success还是error（任意一行失败则为失败）
#             messages.success(request, tips)
#             return render(request, 'upload_case.html')
#         else:
#             messages.error(request, tips)
#             return render(request, 'upload_case.html')


def test_tools(request):
    """测试工具页HTML对应view函数"""
    envs = ['staging', 'test', 'test2', 'test3', 'test4', 'test5', 'test6']
    return render(request, 'test_tools.html', {'envs': envs})


def tools_button(request):
    """测试工具页button对应处理函数"""
    env = request.POST.get('environment')   # 获取选择的测试环境
    so_value = request.POST.get('so_value', '')     # 获取输入的SO单号
    po_value = request.POST.get('po_value', '')     # 获取输入的PO单号
    num = request.POST.get('invoice_num', '')       # 获取输入的发票编号
    order_sku = request.POST.getlist('order_sku', '')    # 获取输入的sku
    order_sku_quantity = request.POST.getlist('order_sku_quantity', '')     # 获取输入的sku数量
    so_cs = request.POST.get('so_cs_value', '')         #获取申请售后的so单号
    cs_type = request.POST.get('cs_type', '')        #获取申请售后的售后类型
    if cs_type == '取消':
        cs_type_other = '请选择'
        cs_type_another = '退货'
    elif cs_type == '退货':
        cs_type_other = '请选择'
        cs_type_another = '取消'
    else:
        cs_type_other = '取消'
        cs_type_another = '退货'
    action = request.POST.get('button')     # 从button的value值分析所需要进行的操作
    if action in ('生成发货单', '生成PO', '西域确认PO', '直发转非直发', '供应商确认', 'PO查询', 'SO开票', '分配库存', 'SO全部发货', '查询', '更新', '售后确认', '售后完结', '售后作废'):
        tt = TestTools(env, so_value, num, po_value, order_sku, order_sku_quantity, so_cs, cs_type, odoo_flag=True)   # test_tools模块类实例
    elif action in ('发货', 'SO查询', 'SO发货'):
        tt = TestTools(env, so_value, num, po_value, order_sku, order_sku_quantity, so_cs, cs_type, odoo_flag=True, odoo_db=True)
    elif action in ('SO单号查询', 'SO售后申请查询', '提交售后申请单'):
        tt = TestTools(env, so_value, num, po_value, order_sku, order_sku_quantity, so_cs, cs_type, oc_db=True)
    else:
        tt = TestTools(env, so_value, num, po_value, order_sku, order_sku_quantity, so_cs, cs_type)
    result = {}
    other = ''      # 需要在message上显示的附加信息，如：PO单号
    envs = ['staging', 'test', 'test2', 'test3', 'test4', 'test5', 'test6']
    envs.remove(env)
    envs.insert(0, env)
    bring_back_vals = {'so_value': so_value, 'envs': envs, 'invoice_value': num, 'po_value': po_value, 'order_sku' : order_sku,
                       'order_sku_quantity' : order_sku_quantity, 'so_cs': so_cs, 'cs_type':cs_type, 'cs_type_other':cs_type_other, 'cs_type_another':cs_type_another}
    if action == '获取Token':
        result = tt.login()
        request.session['token'] = result['sys']['token']
        # print(result)
    if action == '生成订单':    # test_tools模块对应函数
        token = request.session.get('token', '')
        print(token)
        if not token:
            flag = {'flag': 'fail', 'message': 'No Token'}
            bring_back_vals.update(flag)
            return render(request, 'test_tools.html', bring_back_vals)
        result = tt.create_order(token)
        print(result)
        if result['mark'] == '0':
            flag = {'flag': 'success', 'message': result['data']['orderId']}
            bring_back_vals.update(flag)
            return render(request, 'test_tools.html', bring_back_vals)
        else:
            flag = {'flag': 'fail', 'message': result['message']}
            bring_back_vals.update(flag)
            return render(request, 'test_tools.html', bring_back_vals)
    if action == 'SO单号查询':
        ex_no = request.POST.get('ex_no', '')
        result = tt.query_so_no(request)
        bring_back_vals.update({'ex_no': ex_no})
    if action == '订单详情':
        token = request.session.get('token', '')
        if not token:
            flag = {'flag': 'fail', 'message': 'No Token'}
            bring_back_vals.update(flag)
            return render(request, 'test_tools.html', bring_back_vals)
        result = tt.order_detail(token)
        if result['mark'] == '0':
            flag = {'flag': 'success', 'message': json.dumps(result)}
            bring_back_vals.update(flag)
            return render(request, 'test_tools.html', bring_back_vals)
        else:
            flag = {'flag': 'fail', 'message': result['message']}
            bring_back_vals.update(flag)
            return render(request, 'test_tools.html', bring_back_vals)
    if action == '订单取消':
         result = tt.order_cancel()
    if action == '财务收款':
        result = tt.order_payed()
    if action == '确认订单':
        result = tt.order_confirm()
    if action == '分配库存':
        result = tt.create_delivery_allocate()
    if action == '生成PO':
        so = request.POST.get('so_po_value', '')
        bring_back_vals.update({'so_po_value': so})
        result = tt.create_po(request)
        if result['mark'] == '0':
            other = result['po']
    if action == 'SO查询':
        result = tt.query_so_send_detail()
        if result['mark'] == '0':
            bring_back_vals.update({'so_detail': result['send_detail']})
            request.session['so_detail'] = result['send_detail']
    if action == 'SO发货':
        so_detail = request.session.get('so_detail')
        bring_back_vals.update({'so_detail': so_detail})
        result = tt.so_send(request)
    if action == 'SO全部发货':
        so_detail = request.session.get('so_detail')
        bring_back_vals.update({'so_detail': so_detail})
        result = tt.so_send_all(request)
    if action == '西域确认PO':
        result = tt.confirm_po()
    if action == '直发转非直发':
        result = tt.po_change_to_feizhifa()
    if action == '供应商确认':
        result = tt.supplier_confirm()
    if action == 'PO查询':
        result = tt.query_po_send_detail()
        if result['mark'] == '0':
            bring_back_vals.update({'po_detail': result['detail']})
            request.session['po_detail'] = result['detail']
    if action == 'PO发货':
        po_detail = request.session.get('po_detail')
        print(po_detail)
        result = tt.po_send(request)
        bring_back_vals.update({'po_detail': po_detail})
    if action == 'SO开票':
        result = tt.so_invoice()
    if action == 'SO售后申请查询':
        result = tt.query_after_sale_list(request)
        def MyDefault(obj):
            if isinstance(obj, decimal.Decimal):
                return str(obj)
        if result['mark'] == '0':
            if result['available_cs_detail'] == []:
                flag = {'flag': 'fail', 'message': result['message']+'，没有可申请取消或退货的商品'}
                bring_back_vals.update(flag)
                return render(request, 'test_tools.html', bring_back_vals)
            else:
                bring_back_vals.update({'available_cs_detail':result['available_cs_detail']})
                available_cs_detail = json.dumps(result['available_cs_detail'], default=MyDefault)  #转化成json格式
                available_cs_detail = json.loads(available_cs_detail)   #转化成字典格式
                request.session['available_cs_detail'] =available_cs_detail
    if action == '提交售后申请单':
        available_cs_detail = request.session.get('available_cs_detail')
        sku_handle_num = request.POST.getlist('sku_handle_num', '')
        for i in range(len(available_cs_detail)):
            available_cs_detail[i].update({'sku_handle_num':sku_handle_num[i]})
        # print(available_cs_detail)
        bring_back_vals.update({'available_cs_detail': available_cs_detail})
        result = tt.create_after_sale_list(request)
        if result['mark'] == '0':
            other = result['CS_NO']
    if action == '售后确认':
        cs_no = request.POST.get('cs_no', '')
        bring_back_vals.update({'cs_no': cs_no})
        result = tt.after_sale_confirm(request)
    if action == '售后完结':
        cs_no = request.POST.get('cs_no', '')
        bring_back_vals.update({'cs_no': cs_no})
        result = tt.after_sale_done(request)
    if action == '售后作废':
        cs_no = request.POST.get('cs_no', '')
        bring_back_vals.update({'cs_no': cs_no})
        result = tt.after_sale_refuse(request)
    if action == '查询':
        result = tt.query_stock(request)
        sku_stock = request.POST.get('sku_stock', '')
        if result['mark'] == '0':
            bring_back_vals.update({'qty_stock': result['qty'], 'sku_stock': sku_stock})
    if action == '更新':
        result = tt.update_stock(request)
        sku_stock = request.POST.get('sku_stock', '')
        bring_back_vals.update({'sku_stock': sku_stock})
    if result['mark'] == '0':   # 接口返回mark为0表示成功
        flag = {'flag': 'success', 'message': result['message'] + '    ' + other}
        bring_back_vals.update(flag)
        return render(request, 'test_tools.html', bring_back_vals)
    if result['mark'] != '0':   # 接口返回的mark参数不为'0'则提示错误信息
        flag = {'flag': 'fail', 'message': result['message']}
        bring_back_vals.update(flag)
        return render(request, 'test_tools.html', bring_back_vals)




