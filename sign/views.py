# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import apis
import requests, xlrd,xlwt, json, os
from xlwt import Style
from django.contrib import messages
from sign.test_tools import TestTools
import datetime
import decimal

def index(request):
    """index首页"""
    api_list = apis.objects.all()  # 通过objects这个模型管理器的all()获得apis表中所有数据行，相当于SQL中的SELECT * FROM
    return render(request, 'index.html', {'api_list': api_list}) #返回获取的数据行

def api_detail(request):
    """接口详情页"""
    url = request.path   # 获取当前地址url
    loc_start = url.rindex('_')+1    # 从url中获取接口ID的索引位置
    id = url[loc_start:]            # 获取接口ID
    api = apis.objects.get(id=id)   #获取单个对象，通过id值获取数据行
    params_list = (api.params.strip()).split(',')   # 将数据库中params字段值拆分成列表，在HTML上打印出来,.strip()移除首位字符，默认空格
    return render(request, 'api_detail.html', {'api': api, 'params': params_list})


def run_test(request):
    """接口详情-单个接口调用"""
    id = request.POST.getlist('run_button')  # 获取run_button的value值（即接口ID），取得的是列表
    print(id)
    api = apis.objects.get(id=id[0]) #获取单个对象，通过id值获取数据行
    print(api)
    method = api.method.lower()
    print(method)
    url = api.address
    print(url)
    test_data = request.POST.copy()         # copy request请求对象（因为原request请求对象不可更改）
    print(test_data)
    test_data.pop('run_button')  # 只留下输入框填写的数据，去掉带过来的id值
    if method == 'post':
        r = requests.post(url, data=test_data)
        print(r)
    if method == 'get':
        r = requests.get(url, data=test_data)
    result = r.json()
    if result['mark'] == '0':
        messages.success(request, result['message'])
    if result['mark'] != '0':
        messages.error(request, result['message'])
    return render(request, 'api_detail.html', {'api': api, 'test_data': test_data})     # 输入框数据原样返回

def upload_case(request):
    """批量测试HTML对应view函数"""
    return render(request, 'upload_case.html',)


def batch_test(request):
    """批量测试按钮触发的动作函数"""
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            messages.error(request, "no files for upload!")
            return render(request, 'upload_case.html')
        destination = open(os.path.join("./case", myFile.name), 'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        flag = True  # 标志是否有用例失败
        p = 0  # 成功的case数量
        f = 0  # 失败的case数量
        rows_fail = []  # excel中失败行
        fail_reason = []    # 失败原因
        file = './case/'+myFile.name    # 文件路径
        data = xlrd.open_workbook(file)
        table = data.sheet_by_index(0)      # 读取excel sheet页
        rows = table.nrows      # 获取当前sheet页数据行数
        # 接口测试报告
        report = xlwt.Workbook()
        report_table = report.add_sheet('接口测试结果')
        styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour gray50')
        font_color = xlwt.easyxf('font: colour_index red')
        report_table.write(0,0,'序号', styleBlueBkg)
        report_table.write(0, 1, '接口名称', styleBlueBkg)
        report_table.write(0, 2, '接口URL', styleBlueBkg)
        report_table.write(0, 3, 'message', styleBlueBkg)
        report_table.write(0, 4, '执行结果', styleBlueBkg)
        report_table.write(0, 5, '执行时间(s)', styleBlueBkg)
        first_col = report_table.col(1)    # 获取列
        second_col = report_table.col(2)
        third_col = report_table.col(3)
        four_col = report_table.col(5)
        first_col.width = 256*10     # 设置列宽
        second_col.width = 256*50
        third_col.width = 256*10
        four_col.width = 256*15
        report.save('./sign/static/file/report.xls')
        for row in range(1, rows):
            excel_data = table.row_values(row)  # 获取当前行的数据（列表对象）
            url = excel_data[2]
            method = excel_data[3].lower()
            params = excel_data[4]
            message_assert = excel_data[5].strip()      # strip去掉首尾空格
            start_time = datetime.datetime.now()
            if method == 'post':
                params = eval(params)    # excel表中的字符串转换为字典
                r = requests.post(url, data=params)
            if method == 'get':
                params = eval(params)
                r = requests.get(url, params=params)
            end_time = datetime.datetime.now()
            run_time = str(end_time - start_time)[6:10]
            if method != 'post' and method != 'get':
                messages.error(request, 'Method填写错误')
                return render(request, 'upload_case.html')
            result = r.json()
            print(result['message'])
            # 接口测试报告写入
            report_table.write(row,0,row)
            report_table.write(row,1,excel_data[1])
            report_table.write(row, 2, url)
            report_table.write(row, 3, result['message'])
            if result['message'] == message_assert:     # 断言
                p += 1
                report_table.write(row, 4, 'pass')
            else:
                f += 1
                rows_fail.append(str(row + 1))
                fail_reason.append(result['message'])
                report_table.write(row, 4, 'fail', font_color)
            report_table.write(row, 5, run_time)
            report.save('./sign/static/file/report.xls')
        tips = {'成功': p, '失败': f, '失败行数': (','.join(rows_fail) or '无'), '失败原因': (','.join(fail_reason) or '无')}
        if f != 0:
            flag = False
        if flag:    # 根据flag判断message是success还是error（任意一行失败则为失败）
            messages.success(request, tips)
            return render(request, 'upload_case.html')
        else:
            messages.error(request, tips)
            return render(request, 'upload_case.html')


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
        if not token:
            messages.error(request, 'No Token')
            return render(request, 'test_tools.html', bring_back_vals)
        result = tt.create_order(token)
        print(result)
        if result['mark'] == '0':
            messages.success(request, result['data']['orderId'])
            return render(request, 'test_tools.html', bring_back_vals)
        else:
            messages.error(request, result['message'])
            return render(request, 'test_tools.html', bring_back_vals)
    if action == 'SO单号查询':
        ex_no = request.POST.get('ex_no', '')
        result = tt.query_so_no(request)
        bring_back_vals.update({'ex_no': ex_no})
    if action == '订单详情':
        token = request.session.get('token', '')
        if not token:
            messages.error(request, 'No Token')
            return render(request, 'test_tools.html', bring_back_vals)
        result = tt.order_detail(token)
        if result['mark'] == '0':
            messages.success(request, json.dumps(result))
            return render(request, 'test_tools.html', bring_back_vals)
        else:
            messages.error(request, result['message'])
            return render(request, 'test_tools.html', bring_back_vals)
    if action == '订单取消':
        # token = request.session.get('token')
        # if not token:
        #     messages.error(request, 'No token')
        #     return render(request, 'test_tools.html',bring_back_vals)
        # result = tt.order_cancel(token)
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
                messages.success(request, result['message']+'，没有可申请取消或退货的商品')
                return render(request, 'test_tools.html' , bring_back_vals)
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
        messages.success(request, result['message'] + '    ' + other)
        return render(request, 'test_tools.html', bring_back_vals)
    if result['mark'] != '0':   # 接口返回的mark参数不为'0'则提示错误信息
        messages.error(request, result['message'])
        return render(request, 'test_tools.html', bring_back_vals)




