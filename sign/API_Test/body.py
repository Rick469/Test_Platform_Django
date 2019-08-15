    def test_${case_name}(self):
        """${api_name}"""
        url = 'http://${project}${env}.ehsy.com${path}'
        project = '${project}'
        method = '${method}'
        data_type = '${data_type}'
        params = ${params}
        headers = '${headers}'
        depende_flag = ${depende_flag}
        get_response_param = '${get_response_param}'
        use_response_param = '${use_response_param}'
        assert_field = '${assert_field}'
        expectation = '${expectation}'

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
