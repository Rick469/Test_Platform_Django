import requests
import psycopg2, pymysql, json
import time
from django.shortcuts import render
from django.contrib import messages
import sys
import datetime
from xmlrpc import client


class TestTools(object):
    def __init__(self, env, order_id, num, po_id, order_sku, order_sku_quantity, so_cs, cs_type, oc_db=False, odoo_flag=False, odoo_db=False):
        self.env = env       # 测试环境标志： 1 - staging； 0 - test
        self.order_id = order_id        # 传入的SO编号
        self.num = num      # 传入的发票编号
        self.po_id = po_id
        self.order_sku = order_sku  # 传入的sku
        self.order_sku_quantity = order_sku_quantity   # 传入的sku数量
        self.so_cs = so_cs     # 申请售后的订单
        self.cs_type = cs_type    # 申请售后的类型
        if oc_db:
            if self.env == 'staging':
                # 连接staging——OC数据库
                self.connection = pymysql.connect(
                    host='118.178.189.137',
                    user='ehsy_pc',
                    password='ehsy2016',
                    port=3306,
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor   # sql查询结果转为字典类型
                )
            else:
                # test——OC数据库
                self.connection = pymysql.connect(
                    host='118.178.135.2',
                    user='root',
                    password='ehsy2016',
                    port=3306,
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor
                )
        if odoo_flag:
            if self.env == 'staging':
                self.dbname = 'odoo-staging'
                self.usr = 'admin'
                self.pwd = 'admin'
                self.oe_ip = 'odoo-staging.ehsy.com'
                # self.oe_ip = 'localhost:8069'
                self.sock_common = client.ServerProxy('http://' + self.oe_ip + '/xmlrpc/common')
                self.uid = self.sock_common.login(self.dbname, self.usr, self.pwd)
                self.sock = client.ServerProxy('http://' + self.oe_ip + '/xmlrpc/object')
            else:
                self.dbname = 'odoo-test'
                self.usr = 'admin'
                self.pwd = 'admin'
                self.oe_ip = 'odoo-test.ehsy.com'
                # self.oe_ip = 'localhost:8069'
                self.sock_common = client.ServerProxy('http://' + self.oe_ip + '/xmlrpc/common')
                self.uid = self.sock_common.login(self.dbname, self.usr, self.pwd)
                self.sock = client.ServerProxy('http://' + self.oe_ip + '/xmlrpc/object')
        if odoo_db:
            if self.env == 'staging':
                self.con = psycopg2.connect(
                    host='118.178.133.107',
                    port=5432,
                    user='openerp',
                    password='openerp2016',
                    database='odoo-staging',
                )
            else:
                self.con = psycopg2.connect(
                    host='118.178.238.29',
                    port=5432,
                    user='openerp',
                    password='ehsy_erp',
                    database='odoo-test',
                )
            self.cr = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def login(self):
        url = 'http://uc-' + self.env + '.ehsy.com/user/login.action'
        data = {'login_name': '特定用户-不要随意使用', 'login_password': '111qqq', 'terminal_type': 'pc'}
        r = requests.post(url, data=data)
        result = r.json()
        # print(result)
        token = result['sys']['token']
        # print(token)
        return result

    def create_order(self, token):
        """生成订单"""
        url1 = 'http://oc-' + self.env + '.ehsy.com/cart/add'
        # print(self.order_sku, self.order_sku_quantity)
        if self.order_sku[0] == '':
            data1 = [{'skuCode': self.order_sku[1], 'quantity': self.order_sku_quantity[1]}]
        elif self.order_sku[1] == '':
            data1 = [{'skuCode': self.order_sku[0], 'quantity': self.order_sku_quantity[0]}]
        else:
            data1 = [{'skuCode':self.order_sku[0], 'quantity':self.order_sku_quantity[0]}, {'skuCode':self.order_sku[1], 'quantity':self.order_sku_quantity[1]}]
        # print(data1)
        data = {'token': token, 'data' : data1}
        r1 = requests.post(url1, json=data)
        result1 = r1.json()
        # print(result1)
        url2 = 'http://oc-' + self.env + '.ehsy.com/order/createOrderNew'
        addedInvoices = [{"bank": "招商银行", "bankAccount": "2343345466", "hasAdminAuth": "0", "invoiceId": "10008247487",
                         'isDefault': "0",  "regAdd": "金科路1122号", "regTel": "18751551645", "selected": 'true',"subType":'',
                          "taxpayerCode": "123456789009876123", "title": "测试账号公司tina", "type":"2", "typeCompany":'false',
                          'typeDesc': '增值税发票'}]
        deliverAdds = [{ "address":"江苏省南京市高淳县新街口", "addressId": "10008284154", "addressUserType":"1", "areaId":"220",
                         "city":"南京市", "company":"测试账号", "detailedAddress":"新街口", "district":"高淳县",
                         "email":"233213@qq.com", "hasAdminAuth":"0", "isDefault":"1", "mobile":"18751551645", "name":"史佐兄",
                         "postcode":"900414", "province":"江苏省", "selected":'true', "tel":"021-33338888"}]
        invoicesAdds = [{"address":"上海市上海市浦东新区金科路", "addressId":"10008284152", "addressUserType":"1", "areaId":"321",
                         "city":"上海市", "company":"测试账号电子公司", "detailedAddress":"金科路", "district":"浦东新区",
                         "email":"", "hasAdminAuth":"0", "isDefault":"1", "mobile":"18751551645", "name":"史佐兄",
                         "postcode": "900414","province": "上海市", "selected": 'true', "tel":""}]
        data = {'token': token, 'addedInvoices': addedInvoices, 'deliverAdds': deliverAdds, 'deliveryTimeType': '0',
                'invoicesAdds': invoicesAdds, 'payType': '0', 'createFrom': 'pc'}
        r2 = requests.post(url2, json=data)
        result2 = r2.json()  # 字典格式
        # result = json.dumps(result2)  # json格式
        # orderId = result2['data']['orderId']
        return result2

    # def order_detail(self, token, orderId):
    def order_detail(self, token):
        url = 'http://oc-' + self.env + '.ehsy.com/order/getInfo'
        data = {'token': token, 'orderId':self.order_id, 'createTimeFrom':'2017-02-15', 'createTimeTo':'2017-08-15'}
        r = requests.post(url,data)
        result = r.json()
        return result

    def order_cancel(self):
        """查询so中可取消sku"""
        url = 'http://oc-' + self.env + '.ehsy.com/orderCenter/cancel'
        data = {'orderId': self.order_id,'userId':'508110571'}
        r = requests.post(url, data)
        result = r.json()
        return result

    def order_payed(self):
        """财务收款"""
        url = 'http://oc-' + self.env + '.ehsy.com/orderCenter/payed'
        data = {'orderId': self.order_id, 'payWay': '0'}
        r = requests.post(url, data=data)
        result = r.json()
        return result

    def order_confirm(self):
        """SO确认"""
        url = 'http://oc-' + self.env + '.ehsy.com/orderCenter/confirmOrder'
        data = {"orderId": self.order_id}
        r = requests.post(url, data=data)
        result = r.json()
        return result

    def create_delivery_allocate(self):
        vals = {
            'so': self.order_id
        }
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'test_button_create_delivery', vals)
        return result

    def create_po(self, request):
        """创建PO"""
        so = request.POST.get('so_po_value', '')
        if not so:
            return {'mark': '1', 'message': '请输入SO单号！'}
        vals = {
            'so': so
        }
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'test_create_po', vals)
        return result

    def confirm_po(self):
        """西域确认PO"""
        vals = {
            'po': self.po_id
        }
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'test_ehsy_button_approve', vals)
        return result

    # def po_change_to_zhifa(self):
    #     """PO单非直发转直发"""
    #     cursor = self.connection.cursor()
    #     cursor.execute("select pur_order_id from oc.purchase_order where order_id= '"+self.order_id+"'")
    #     po = cursor.fetchall()[0]['pur_order_id']   # 获取PO单号
    #     url = 'http://oc-' + self.env + '.ehsy.com/admin/purchaseorder/poChangeNonStopFlag'
    #     r = requests.post(url, data={
    #         'purOrderId': po, 'nonStopFlag': '1'})
    #     result = r.json()
    #     return result

    def po_change_to_feizhifa(self):
        """直发转非直发"""
        vals = {
            'po': self.po_id
        }
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'test_action_po_district', vals)
        return result

    def supplier_confirm(self):
        """供应商确认"""
        vals = {
            'po': self.po_id
        }
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'test_button_approve', vals)
        return result

    def query_po_send_detail(self):
        """查询PO发货详情"""
        vals = {
            'purOrderId': self.po_id
        }
        query_result = self.sock.execute(self.dbname, self.uid, self.pwd, 'purchase.order', 'get_po_info_spc', json.dumps(vals))
        query_result = json.loads(query_result)
        if query_result['mark'] == '1':
            result = query_result
        elif query_result['mark'] == '0':
            result = {'mark': '0', 'message': 'Success'}

            # 组装采购单详情数据
            detail = []
            for i in query_result['data']['purchaseOrderUnitList']:
                detail_dic = {}
                detail_dic['sku'] = i['skuCode']
                detail_dic['qty'] = i['quantity']
                detail_dic['send_qty'] = i['sendedQuantity']
                detail.append(detail_dic)
            result['detail'] = detail
        return result

    def po_send(self, request):
        """PO发货"""
        vals = {}
        sku_list = request.POST.getlist('sku', '')
        pre_send_qty = request.POST.getlist('pre_send_qty', '')
        send_no = request.POST.get('send_no', '')
        send_company = request.POST.get('send_company', '')
        if not (any(sku_list) and any(pre_send_qty) and send_company):
            result = {'mark': '1', 'message': '数据填写不完整'}
            return result
        if send_company != '自送' and send_no == '':
            result = {'mark': '1', 'message': '非自送运单号不能为空'}
            return result
        self.cr.execute(
            "select b.guid from public.purchase_order a join res_partner b on a.partner_id=b.id where a.name='" + self.po_id + "'"
        )
        info = self.cr.fetchone()
        if not info:
            return {'mark': '1', 'message': '找不到对应的PO单号'}
        vals['purOrderId'] = self.po_id
        vals['supplierId'] = info[0]
        vals['sendNo'] = send_no
        vals['sendCompanyName'] = send_company

        deliveryList = []
        for i in range(len(sku_list)):
            if pre_send_qty[i]:
                send_detail = {}
                send_detail['skuCode'] = sku_list[i]
                print(sku_list[i])
                send_detail['sendQuantity'] = int(pre_send_qty[i])
                self.cr.execute(
                    "select a.product_uom, a.product_name, a.so_no, a.id, a.partner_id from public.purchase_order_line a where a.order_id=(select id from public.purchase_order where name='" + self.po_id + "') and a.product_code='"+sku_list[i]+"'"
                )
                sql_result = self.cr.fetchone()
                print('sql_result: %s' % sql_result)
                self.cr.execute(
                    "select name from public.product_uom where id='"+str(sql_result[0])+"'"
                )
                unit = self.cr.fetchone()
                print('unit: %s' % unit)
                send_detail['productName'] = sql_result[1]
                send_detail['unit'] = unit[0]
                send_detail['orderId'] = sql_result[2]
                send_detail['id'] = sql_result[3]
                deliveryList.append(send_detail)
            else:
                continue
        vals['deliveryList'] = deliveryList
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'supplier.purchase.order.delivery', 'get_po_delivery', json.dumps(vals))
        result = json.loads(result)
        if result['mark'] == '0':
            result['message'] = 'Success'
        return result

    def so_invoice(self):
        """SO开票-Odoo"""
        if not self.order_id:
            return {'mark': '1', 'message': 'SO单号不能为空！'}
        vals = {'so': self.order_id, 'env': self.env}
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'so_invoice', vals)
        return result

    def query_so_send_detail(self):
        """查询SO发货详情"""
        self.cr.execute(
            "select a.product_uom_qty, a.cancel_qty, a.qty_delivered, a.product_id from public.sale_order_line a where a.name !='运费' and a.order_id=(select id from public.sale_order where name='"+self.order_id+"')"
        )
        order_line = self.cr.fetchall()
        if not order_line:
            return {'mark': '1', 'message': '找不到对应的SO单号'}
        send_detail = []
        for i in order_line:
            sku_detail = {}
            self.cr.execute(
                "select default_code from public.product_product where id='"+str(i[3])+"'"
            )
            sku = self.cr.fetchone()
            sku_detail['sku'] = sku[0]
            sku_detail['k_send_qty'] = str(int(i[0]-i[1]))  # 原数量
            sku_detail['y_send_qty'] = str(i[2])            # 已发货数量
            send_detail.append(sku_detail)
        result = {'mark': '0', 'message': 'Success', 'send_detail': send_detail}
        return result

    def so_send(self, request):
        """SO发货--按输入的数量发货"""
        vals = {}
        sku_list = request.POST.getlist('so_sku', '')
        send_qty_list = request.POST.getlist('so_send_qty', '')
        send_no = request.POST.get('so_send_no', '')
        send_company = request.POST.get('so_send_company', '')
        env = self.env

        if not (self.order_id and send_no and any(send_qty_list) and env):
            return {'mark': '1', 'message': '数据填写不完整'}
        vals['so'] = self.order_id
        vals['batch_flag'] = 'true'
        vals['send_no'] = send_no
        # vals['send_company'] = send_company
        send_detail = []

        # 组装发货明细参数send_detail
        for i in range(len(sku_list)):
            if send_qty_list[i]:
                detail = {}
                detail['sku'] = sku_list[i]
                detail['send_qty'] = send_qty_list[i]
                send_detail.append(detail)
            else:
                continue
        vals['send_detail'] = send_detail

        vals['env'] = env
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'test_so_transfer', vals)
        return result

    def so_send_all(self, request):
        """SO全部发货"""
        vals = {}
        send_no = request.POST.get('so_send_no', '')
        env = self.env
        if not (self.order_id and send_no and env):
            return {'mark': '1', 'message': '数据填写不完整'}
        vals['so'] = self.order_id
        vals['batch_flag'] = 'false'    # 分批发货标志，false:全部发货； true部分发货
        vals['send_no'] = send_no
        vals['env'] = env
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'test_so_transfer', vals)
        return result

    def query_stock(self, request):
        """查询odoo库存"""
        sku = request.POST.get('sku_stock', '')
        if not sku:
            return {'mark': '1', 'message': 'SKU不能为空'}
        vals = {'product': sku}
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'query_product_qty', vals)
        return result

    def update_stock(self, request):
        """更新odoo库存"""
        sku = request.POST.get('sku_stock', '')
        update_qty = request.POST.get('qty_stock', '')
        if not sku:
            return {'mark': '1', 'message': 'SKU不能为空'}
        if not update_qty:
            return {'mark': '1', 'message': '更新数量不能为空'}
        vals = {'product': sku, 'update_qty': update_qty}
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'update_product_qty', vals)
        return result

    def after_sale_confirm(self, request):
        """售后确认"""
        cs_no = request.POST.get('cs_no', '')
        if not cs_no:
            return {'mark': '1', 'message': 'CS_No不能为空'}
        vals = {'cs_no': cs_no, 'env': self.env}
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'after_sale_confirm', vals)
        return result

    def query_after_sale_list(self, request):
        """查询可申请售后商品"""
        so_cs = request.POST.get('so_cs_value', '')
        cs_type = request.POST.get('cs_type', '')
        cr = self.connection.cursor()
        if cs_type == '请选择':
            return {'mark':'1', 'message':'请选择售后类型'}
        if so_cs == '':
            return {'mark': '1', 'message': '请输入申请售后的SO单号'}
        if cs_type == '取消' and so_cs != '':
            cr.execute("select a.sku_code, (a.quantity-a.send_quantity) as avaliable_cancle_num from oc.order_detail a where a.order_id = '"+ so_cs+"'")
            cr_r = cr.fetchall()
            cr.execute("select c.sku_code, c.quantity from oc.cs_apply_detail c where c.cs_no in (select b.cs_no from oc.cs_apply b where b.cs_status=0 and b.ORDER_ID = '"+ so_cs +"' and b.cs_type=9)")
            cr_2 = cr.fetchall()
            for i in cr_r:
                for j in cr_2:
                    if i['sku_code'] == j['sku_code']:
                        i['avaliable_cancle_num'] = i['avaliable_cancle_num'] - j['quantity']
            # print(cr_r, cr_2)
        if cs_type == '退货' and so_cs != '':
            cr.execute("select a.sku_code, a.send_quantity as avaliable_cancle_num from oc.order_detail a where a.order_id = '"+ so_cs+"'")
            cr_r = cr.fetchall()
            cr.execute("select b.sku_code, b.quantity from oc.cs_apply_detail b where b.CS_NO in (select a.CS_NO from oc.cs_apply a where a.order_id = '"+ so_cs +"' and a.CS_TYPE = 0 and a.CS_STATUS =0) and b.CS_TYPE =0")
            cr_1 = cr.fetchall()
            cr.execute("select b.sku_code, b.quantity from oc.cs_apply_detail b where b.CS_NO in (select a.CS_NO from oc.cs_apply a where a.order_id = '"+ so_cs +"' and a.CS_TYPE = 0 and a.CS_STATUS in(1,99)) and b.CS_TYPE =1")
            cr_2 = cr.fetchall()
            for i in cr_r:
                for j in cr_1:
                    if i['sku_code'] == j['sku_code']:
                        i['avaliable_cancle_num'] = i['avaliable_cancle_num'] - j['quantity']
            for i in cr_r:
                for j in cr_2:
                    if i['sku_code'] == j['sku_code']:
                        i['avaliable_cancle_num'] = i['avaliable_cancle_num'] - j['quantity']
        list = []
        for i in cr_r:
            if int(i['avaliable_cancle_num']) >= 1 :
                list.append(i)
        # print(list)
        return {'mark':'0', 'message':'查询成功', 'available_cs_detail':list}

    def create_after_sale_list(self, request):
        """创建售后申请单"""
        cs_type = request.POST.get('cs_type', '')
        so_cs = request.POST.get('so_cs_value', '')
        order_available_sku = request.POST.getlist('order_available_sku', '')
        sku_handle_num = request.POST.getlist('sku_handle_num', '')
        dictionary = dict(zip(order_available_sku, sku_handle_num))
        list = []
        cr = self.connection.cursor()
        if not any(sku_handle_num):
            return {'mark' : '1', 'message' : '请正确填写申请取消或退货的商品数量'}
        else:
            for i in dictionary.items():
                if i[1] != '' and i[1] != 0:
                    cr.execute("select a.sku_code as skuCode, a.brand_Name as brandName, a.product_Name as productName, a.unit, a.product_Pic as productPic, a.product_Model as productModel, a.sale_Price as salePrice from oc.order_detail a "
                        "where a.order_id = '"+ so_cs +"' and a.sku_code = '"+ i[0] +"'" )
                    self.connection.commit()
                    cr_r = cr.fetchall()
                    data_sku = {"quantity":i[1], "refundAmt":"","reparationAmt":"","warehouseCode":"","worthless":"","transferAmount":"","returnToSupplier":0,"remark":"test"}
                    data_sku.update(cr_r[0])
                    a  = data_sku['salePrice']
                    data_sku['salePrice'] = float(a)
                    list.append(data_sku)
            if cs_type == '取消':
                url = 'http://oc-' + self.env + '.ehsy.com/admin/cs/saveCSApplyAndDetailOnly'
                data = {"csType":9,"orderId":so_cs,"actualDetailList":list, "userId":"admin","createUserName":"\u897f\u57dfOPC"}
                # 参数为表单用户data=；参数为json串用json=或data=json.dumps()
                r = requests.post(url, data=json.dumps(data))
                result = r.json()
            if cs_type == '退货':
                url = 'http://oc-' + self.env + '.ehsy.com/admin/cs/saveCSApplyAndDetailOnly'
                data = {"csType":0,"orderId":so_cs,"actualDetailList":[data_sku], "userId":"admin","createUserName":"\u897f\u57dfOPC"}
                r = requests.post(url, json=data)
                result = r.json()
            # cr = self.connection.cursor()
            cr.execute("select a.CS_NO from oc.cs_apply a where a.order_id = '"+ so_cs +"' ORDER BY a.CREATE_TIME DESC limit 1")
            cr_r = cr.fetchall()
            result.update(cr_r[0])
        return result

    def after_sale_done(self, request):
        """售后申请完结"""
        cs_no = request.POST.get('cs_no', '')
        if not cs_no:
            return {'mark': '1', 'message': 'CS_No不能为空'}
        vals = {'cs_no': cs_no, 'env': self.env}
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'after_sale_done', vals)
        return result

    def after_sale_refuse(self, request):
        """售后申请作废"""
        cs_no = request.POST.get('cs_no', '')
        if not cs_no:
            return {'mark': '1', 'message': 'CS_No不能为空'}
        vals = {'cs_no': cs_no, 'env': self.env}
        result = self.sock.execute(self.dbname, self.uid, self.pwd, 'used.by.tester', 'after_sale_refuse', vals)
        return result

    def query_so_no(self, request):
        """通过外部订单号查询SO单号"""
        ex_no = request.POST.get('ex_no', '')
        if not ex_no:
            return {'mark': '1', 'message': '外部订单号不能为空！'}
        cr = self.connection.cursor()
        cr.execute(
            "select a.order_id from oc.order_info a where a.EXTERNAL_ORDER_NO ='"+ex_no+"'"
        )
        cr_r = cr.fetchone()
        print(cr_r)
        if not cr_r:
            return {'mark': '1', 'message': '没有找到对应订单！'}
        result = {'mark': '0', 'message': '查询成功！ SO单号：'+cr_r['order_id']}
        result.update(cr_r)
        return result
