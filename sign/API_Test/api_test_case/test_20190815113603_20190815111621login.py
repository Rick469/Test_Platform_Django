# -*- coding: gbk -*-
import unittest
from BeautifulReport import BeautifulReport
from run.run import run_case


class Test_20190815111621login (unittest.TestCase):

    def test_login_loginNameError(self):
        """��¼"""
        url = 'http://UC-staging.ehsy.com/user/login.action'
        project = 'UC'
        method = 'POST'
        data_type = 'DATA'
        params = {"login_name":"8CDB10B7FE950DED77409F8AB1AF9B45335205D20A7796595A5AAD86C146CF53","login_password":"111qqq"}
        headers = ''
        depende_flag = 1
        get_response_param = ''
        use_response_param = 'token'
        assert_field = 'message'
        expectation = '��¼�ɹ�'

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
        """��¼"""
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
        expectation = '��¼�ɹ�'

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
        """��¼"""
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
        expectation = '��¼�ɹ�'

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

