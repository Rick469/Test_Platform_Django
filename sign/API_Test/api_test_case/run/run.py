import requests
from sign.models import Dependency


# 执行接口测试
def run_case(data):

    url = data['url']
    project = data['project']
    method = data['method']
    data_type = data['data_type']
    params = data['params']
    headers = data['headers']
    depende_flag = data['depende_flag']
    get_response_param = data['get_response_param']
    use_response_param = data['use_response_param']
    assert_field = data['assert_field']
    expectation = data['expectation']

    if method == 'GET':
        r = requests.get(url, params, headers=headers)
        result = r.json()
    if method == 'POST':
        if data_type == 'JSON':
            r = requests.post(url, json=params, headers=headers)
            result = r.json()
        elif data_type == 'DATA':
            r = requests.post(url, data=params, headers=headers)
            result = r.json()
    print('接口返回response: %s' % result)
    print('expectation: %s' % expectation)

    assert result[assert_field] == expectation

    # 存取返回值
    if depende_flag:
        # 若存在get_response_param则存入数据库留用
        if get_response_param:
            get_response_params = get_response_param.split(',')     # 可能有多个需存储参数，以,分割成list循环存入数据库
            for p in get_response_params:
                db_param = p.split('.')     # 参数可能存在于response多层字典结构内部，逐层提取出来
                value = result
                for i in range(len(db_param)):  # 循环结束后可取出最终存入数据库的param和value
                    param = db_param[i]
                    value = value[param]
                # 参数数据库已存在则更新记录
                record = Dependency.objects.filter(param=param)
                if record:
                    record = record[0]
                    record.value = value
                    record.save()
                # 不存在则创建
                else:
                    Dependency.objects.create(param=param, value=value)
