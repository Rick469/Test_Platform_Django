# -*- coding: gbk -*-
import unittest
from BeautifulReport import BeautifulReport
from run.run import run_case


class Test_20190815111621login (unittest.TestCase):

    def test_login_loginNameError(self):
        """login_loginNameError"""
        url = 'http://UC-staging.ehsy.com/user/login.action'
        project = 'UC'
        method = 'POST'
        data_type = 'DATA'
        params = {"login_name":"8CDB10B7FE950DED77409F8AB1AF9B45D320EA3264E0FBEB623A7BE2D9D4A97D","login_password":"111qqq"}
        headers = ''
        depende_flag = 1
        get_response_param = ''
        use_response_param = 'token'
        assert_field = 'message'
        expectation = '登录成功'

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

    def test_login_store_token_message(self):
        """login_store_token_message"""
        url = 'http://UC-staging.ehsy.com/user/login.action'
        project = 'UC'
        method = 'POST'
        data_type = 'DATA'
        params = {"login_name":"guodiantest","login_password":"111qqq"}
        headers = ''
        depende_flag = 1
        get_response_param = 'sys.token,message'
        use_response_param = ''
        assert_field = 'message'
        expectation = '登录成功'

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

    def test_login(self):
        """login"""
        url = 'http://UC-staging.ehsy.com/user/login.action'
        project = 'UC'
        method = 'POST'
        data_type = 'DATA'
        params = {"login_name":"guodiantest","login_password":"111qqq"}
        headers = ''
        depende_flag = 0
        get_response_param = ''
        use_response_param = ''
        assert_field = 'message'
        expectation = '登录成功'

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
    cases = unittest.defaultTestLoader.discover(r'C:\Users\rick_zhang\Desktop\Test_Platform\sign/API_Test/api_test_case/', pattern='20190815111621login.py')
    result = BeautifulReport(cases).report(filename='Report-20190815111621login.html', description='API-AutoTest-Report', log_path=r'C:\Users\rick_zhang\Desktop\Test_Platform\sign//static/api_test_file/api_test_report/')

