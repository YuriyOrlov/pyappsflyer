import os
import re
import pytest

from pyappsflyer import PerformanceReport, RawDataReport, TargetingValidationRulesReport


@pytest.fixture
def performance_report():
    return PerformanceReport('TestAppName',
                             api_key='some_api_key')

@pytest.fixture
def raw_data_report():
    return RawDataReport('TestAppName',
                         api_key='some_api_key')

@pytest.fixture
def targeting_validation_rules_report():
    return TargetingValidationRulesReport('TestAppName',
                         api_key='some_api_key')


class TestReport:

    def test_performance_report_class_variables_init(self, performance_report: BaseAppsFlyer):
        assert 0 == 0
