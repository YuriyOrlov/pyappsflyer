import os
import re
import pytest

from pyappsflyer.base import BaseAppsFlyer

from unittest.mock import patch, MagicMock

from pyappsflyer.exceptions import PyAFError, PyAFValidationError,\
    PyAFCommunicationError, PyAFUnknownError, WebServerError,\
    AuthenticationError, PyAFProcessingError
from pyappsflyer.base import get_random_filename

from unittest.mock import patch
from io import StringIO

sample_report_names = [
        'partners_report', 'partners_by_date_report',
        'daily_report', 'geo_report', 'geo_by_date_report'
    ]

csv_example = StringIO("""
    test_column1,test_column2,test_column3
    Row 1 col 1,Row 1 col 2,Row 1 col 3
    Row 2 col 1,Row 2 col 2,Row 2 col 3
    Row 3 col 1,Row 3 col 2,Row 3 col 3
""")


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

    def test_validate_dates_and_report_names(self, baseappclass: BaseAppsFlyer):

        with pytest.raises(PyAFValidationError) as e:
            baseappclass.validate_dates_and_report_names('unknown_report',
                                                         sample_report_names, '2018-10-10', '2018-10-11')
        assert 'No such report name in API documentation.' in str(e.value)

        with pytest.raises(PyAFValidationError) as e:
            baseappclass.validate_dates_and_report_names('geo_report',
                                                         sample_report_names, '2018/10/10', '2018-10-11')
        assert 'Date format is invalid' in str(e.value)

        with pytest.raises(PyAFValidationError) as e:
            baseappclass.validate_dates_and_report_names('geo_report',
                                                         sample_report_names, '2018/10/10', '2018/10/11')
        assert 'Date format is invalid' in str(e.value)

        with pytest.raises(PyAFValidationError) as e:
            baseappclass.validate_dates_and_report_names('geo_report',
                                                         sample_report_names, '2018-10-10', '2018/10/11')
        assert 'Date format is invalid' in str(e.value)

    def test_random_filename_creation(self, baseappclass: BaseAppsFlyer):
        uuid4hex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_check = os.path.abspath(f'{base_dir}/../')

        filename_w_path = get_random_filename()

        get_uuid = uuid4hex.search(filename_w_path)
        assert get_uuid is not None
        uuid = get_uuid.group(0)
        filename = f'{uuid}.csv'
        assert filename in filename_w_path
        assert path_to_check.lower() in filename_w_path

        test_filename = 'some_filename.csv'
        filename_w_path = get_random_filename(filename=test_filename)
        assert test_filename in filename_w_path

        test_filename = 'some_filename.ggg'
        filename_w_path = get_random_filename(filename=test_filename)
        assert 'csv' in filename_w_path
        assert '.ggg' not in filename_w_path

    # @patch('requests.get', MagicMock(return_value=csv_example))
    # def test_receiving_csv_file(self, baseappclass: BaseAppsFlyer):
    #     baseappclass.api_report_name = 'geo_report'
    #     result = baseappclass._get_csv()
    #
    #     assert result == ''
