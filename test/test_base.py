import pytest

from pyappsflyer.base import BaseAppsFlyer


@pytest.fixture
def baseappclass():
    return BaseAppsFlyer('BaseTestAppName',
                         api_key='some_api_key')


class TestBase:

    def test_base_class_variables_init(self, baseappclass: BaseAppsFlyer):
        assert baseappclass.logger is not None
        assert baseappclass.api_key == 'some_api_key'
        assert baseappclass.api_url == 'https://hq.appsflyer.com'
        assert baseappclass.api_report_name is None
        assert baseappclass.api_version == 'v5'
        assert baseappclass.api_action == 'export'

    def test_url_preparation(self, baseappclass: BaseAppsFlyer):
         baseappclass.api_report_name = 'some_report_name'
         url_to_go = baseappclass._prepare_url()

         assert str(url_to_go) ==\
                'https://hq.appsflyer.com/export/BaseTestAppName/some_report_name/v5?api_token=some_api_key'

         url_w_addtitional_args = baseappclass._prepare_url(request_args={'some_v': 'args',
                                                                          'readonly':'true'})

         assert str(url_w_addtitional_args) ==\
                'https://hq.appsflyer.com/export/BaseTestAppName/some_report_name/v5?api_token=some_api_key&some' \
                '_v=args&readonly=true'

    def test_csv_file_not_empty(self):
        pass

