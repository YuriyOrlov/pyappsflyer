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

    def test_performance_report_class_variables_init(self, performance_report: PerformanceReport):
        assert performance_report.logger is not None
        assert performance_report.api_key == 'some_api_key'
        assert performance_report.api_url == 'https://hq.appsflyer.com'
        assert performance_report.api_report_name is None
        assert performance_report.api_version == 'v5'
        assert performance_report.api_action == 'export'

        assert len(performance_report.report_names) == 5

    def test_raw_data_report_class_variables_init(self, raw_data_report: RawDataReport):
        assert raw_data_report.logger is not None
        assert raw_data_report.api_key == 'some_api_key'
        assert raw_data_report.api_url == 'https://hq.appsflyer.com'
        assert raw_data_report.api_report_name is None
        assert raw_data_report.api_version == 'v5'
        assert raw_data_report.api_action == 'export'

        assert len(raw_data_report.additional_fields_uninstall_query) == 5
        assert len(raw_data_report.additional_fields) == 11
        assert len(raw_data_report.special_report_names) == 1
        assert len(raw_data_report.report_names) == 5
        assert len(raw_data_report.report_with_retargeting) == 2

    def test_targeting_validation_rules_report_class_variables_init(self,
                                                                    targeting_validation_rules_report:
                                                                    TargetingValidationRulesReport):
        assert targeting_validation_rules_report.logger is not None
        assert targeting_validation_rules_report.api_key == 'some_api_key'
        assert targeting_validation_rules_report.api_url == 'https://hq.appsflyer.com'
        assert targeting_validation_rules_report.api_report_name is None
        assert targeting_validation_rules_report.api_version == 'v5'
        assert targeting_validation_rules_report.api_action == 'export'

        assert len(targeting_validation_rules_report.additional_fields) == 11
        assert len(targeting_validation_rules_report.report_names) == 2