# -*- coding: gbk -*-
import unittest
from BeautifulReport import BeautifulReport
from run.run import run_case


class Test_20190815113556get_product_pool_list (unittest.TestCase):

    def test_mall_login(self):
        """国电商城-登录"""
        url = 'http://SP-staging.ehsy.com/accessToken'
        project = 'SP'
        method = 'POST'
        data_type = 'JSON'
        params = {
    "grant_type": "access_token",
    "client_id": "9852a802d6fe431e9eb85f613ac1e16a",
    "client_secret": "RYXiK2bGS443bKplh7CCnuharR9QmcVW",
    "timestamp": "2019-05-22",
    "username": "guodian",
    "password": "18E1FB2DE8371B2EAAE108D988628544"
}
        headers = ''
        depende_flag = 1
        get_response_param = 'result.access_token'
        use_response_param = ''
        assert_field = 'resultMessage'
        expectation = '获取accessToken成功'

        data = {
                'url': url,
                'project': project,
                'method': method,
                'data_type': data_type,
                'params': params,
                'headers': headers,
                'depende_flag': depende_flag,
                'get_response_param': get_response_param,
                'use_response_param': use_response_param,
                'assert_field': assert_field,
                'expectation': expectation
        }
        run_case(data)

    def test_get_product_pool_list(self):
        """国电标准-获取对接双方划定的商品池列表"""
        url = 'http://SP-staging.ehsy.com/guodianmall/getPageNum'
        project = 'SP'
        method = 'POST'
        data_type = 'JSON'
        params = {
    "token": "696525de-00da-4b26-9682-02014f326555"
}
        headers = ''
        depende_flag = 1
        get_response_param = ''
        use_response_param = 'access_token'
        assert_field = 'resultMessage'
        expectation = '查询成功'

        data = {
                'url': url,
                'project': project,
                'method': method,
                'data_type': data_type,
                'params': params,
                'headers': headers,
                'depende_flag': depende_flag,
                'get_response_param': get_response_param,
                'use_response_param': use_response_param,
                'assert_field': assert_field,
                'expectation': expectation
        }
        run_case(data)

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    cases = unittest.defaultTestLoader.discover(r'C:\Users\rick_zhang\Desktop\Test_Platform\sign/API_Test/api_test_case/', pattern='20190815113556get_product_pool_list.py')
    result = BeautifulReport(cases).report(filename='Report-20190815113556get_product_pool_list.html', description='API-AutoTest-Report', log_path=r'C:\Users\rick_zhang\Desktop\Test_Platform\sign//static/api_test_file/api_test_report/')

