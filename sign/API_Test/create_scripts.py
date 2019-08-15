import requests, xlrd, datetime
from string import Template
from pathlib import Path
from sign.config.path import api_test_case_dir
from sign.config.path import api_report_dir
from sign.models import Dependency
from django.conf import settings
import os


class Create():

    def __init__(self, file_name, sequence):   # file_name为文件对象
        sheet = xlrd.open_workbook(os.path.join(settings.BASE_DIR, 'sign/static/api_test_file/case_file/'+file_name)).sheet_by_index(0)
        row_num = sheet.nrows
        self.data = []  # Excel所有行项目数据字典集--list类型
        for i in range(1, row_num):
            row = sheet.row_values(i)
            self.data.append({
                'case_name': row[0],
                'api_name': row[1],
                'project': row[2],
                'path': row[3],
                'method': row[4],
                'data_type': row[5],
                'params': row[6],
                'headers': row[7],
                'depende_flag': row[8],
                'get_response_param': row[9],
                'use_response_param': row[10],
                'assert_field': row[11],
                'expectation': row[12].strip()
            })
        self.file_name = file_name.split('.')[0]    # 按.分割xxx.xls文件名，去除后缀文件类型
        self.sequence = sequence    # 序列号，外部传入，标识测试任务所属批次(同一sequence脚本为同一批次生成)

    # 校验Excel数据
    def check_data(self):
        assert self.method in ('GET', 'POST')
        if self.method == 'POST':
            assert self.data_type in ('JSON', 'DATA')

    # 循环生成test_case（body结构）
    def loop_body(self, f_body, env):
        code_body = ''

        for row in self.data:   # row:f_body模板替换的参数
            row.update({'env': env})    # 设置执行的测试环境

            # 若存在接口依赖且使用返回值
            if row['depende_flag'] and row['use_response_param']:
                # 传入的需要使用的返回值字段--字符串转为列表批量查询数据库记录
                fields = row['use_response_param'].split(',')
                records = Dependency.objects.filter(param__in=fields).values('param', 'value')  # 返回元素为字典的list,例:[{'param':'param1', 'value':'value1'}]
                if len(records)!=len(fields):
                    raise ValueError('部分使用返回值的变量数据库不存在或有多个')

                replace = {}    # replace: params模板替换的参数
                for record in records:
                    replace.update({record['param']: record['value']})
                row['params'] = Template(row['params']).substitute(replace)
            code_body += Template(f_body).substitute(row)+'\n'
        return code_body

    # 生成测试脚本文件
    def make_test_script(self, env):
        py_name = 'test_' + self.sequence + '_' + self.file_name + '.py'
        file = Path(api_test_case_dir + py_name)
        env = '-'+env if env in ('staging', 'test') else ''

        # 若测试脚本文件不存在则新增
        # if not file.exists():
            # now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        with open(file, 'a+') as f:

            # head = os.path.join(os.path.dirname(__file__), './head.py')
            head = os.path.join(settings.BASE_DIR, 'sign/API_Test/head.py')
            body = os.path.join(settings.BASE_DIR, 'sign/API_Test/body.py')
            footer = os.path.join(settings.BASE_DIR, 'sign/API_Test/footer.py')

            with open(head, 'r') as f_head:
                f_head = f_head.read()
                code_head = Template(f_head).substitute({'class_name': self.file_name})
                f.write(code_head+'\n')
            with open(body, 'r') as f_body:
                f_body = f_body.read()
                code_body = self.loop_body(f_body, env)
                f.write(code_body)
            with open(footer, 'r') as f_footer:
                f_footer = f_footer.read()
                code_footer = Template(f_footer).substitute(case_file=self.file_name+'.py',
                                                            report_name=self.file_name,
                                                            api_test_case_dir=api_test_case_dir,
                                                            api_report_dir=api_report_dir)
                f.write(code_footer)
        # else:   # 脚本文件存在则不处理
        #     print('-----------scripts已存在--------------')
        #     pass
        return py_name


if __name__ == '__main__':
    b = Create('temp.xls')
    b.make_test_script()
