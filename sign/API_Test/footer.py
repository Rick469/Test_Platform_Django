    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    cases = unittest.defaultTestLoader.discover(r'${api_test_case_dir}', pattern='${case_file}')
    result = BeautifulReport(cases).report(filename='Report-${report_name}.html', description='API-AutoTest-Report', log_path=r'${api_report_dir}')

