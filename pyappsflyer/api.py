import logging

from logging.config import dictConfig
from .base import BaseAppsFlyer

from .settings import LOGGING, DEFAULT_TIMEZONE

dictConfig(LOGGING)

logger = logging.getLogger(__name__)


class PerformanceReport(BaseAppsFlyer):

    report_names = (
        'partners_report', 'partners_by_date_report',
        'daily_report', 'geo_report', 'geo_by_date_report'
    )

    def get_report(self,
                   from_date=None,
                   to_date=None,
                   timezone=DEFAULT_TIMEZONE,
                   api_report_name="partners_report",
                   return_dict=True):
        """
        Method to receive one performance report.
        If dates are not presented default number of days will be used.

        :param from_date: from what date to begin, date format - YYYY-MM-DD
        :param to_date: at what date to end, date format - YYYY-MM-DD
        :param timezone: timezone for api request, default - Europe/Moscow
        :param api_report_name: name of the performance report according to api documentation
        :param return_dict: return answer in dict or list
        :return: Ordered dictionary created from CSV file or list created from CSV file
        """
        api_report_name, from_date, to_date = self.validate_dates_and_report_names(api_report_name,
                                                                                   self.report_names,
                                                                                   from_date,
                                                                                   to_date)
        self.api_report_name = api_report_name

        if not from_date or not to_date:
            from_date, to_date = self.get_default_dates()

        return self._get_csv(request_args={"from": from_date,
                                           "to": to_date,
                                           "timezone": timezone},
                             return_dict=return_dict)

    def get_reports(self,
                    *args,
                    **kwargs):

        all_reports = list()

        for report_name in self.report_names:
            all_reports.append({report_name: self.get_report(api_report_name=report_name, *args, **kwargs)})

        return all_reports


class RawDataReport(BaseAppsFlyer):

    additional_fields_uninstall_query = (
        "gp_referrer", "gp_click_time",
        "gp_install_begin", "amazon_aid", "keyword_match_type"
    )

    additional_fields = (
        "install_app_store", "contributor1_match_type",
        "contributor2_match_type", "contributor3_match_type",
        "match_type", "device_category",
    ) + additional_fields_uninstall_query

    special_report_names = (
        'uninstall_events_reports',
    )

    report_names = (
        'installs_report',
        'in_app_events_report',
    ) + special_report_names

    report_with_retargeting = (
        'installs_report',
        'in_app_events_report'
    )

    def get_report(self,
                   from_date=None,
                   to_date=None,
                   timezone=DEFAULT_TIMEZONE,
                   api_report_name="installs_report",
                   return_dict=True,
                   retargeting=False,
                   different_additional_fields=False
                   ):
        api_report_name, from_date, to_date = self.validate_dates_and_report_names(api_report_name,
                                                                                   self.report_names,
                                                                                   from_date,
                                                                                   to_date)
        self.api_report_name = api_report_name

        if not from_date or not to_date:
            from_date, to_date = self.get_default_dates()

        request_args = {"from": from_date,
                        "to": to_date,
                        "timezone": timezone,
                        "additional_fields": ",".join(self.additional_fields)}

        if different_additional_fields:
            request_args["additional_fields"] = ",".join(self.additional_fields_uninstall_query)

        if retargeting:
            request_args.update({"reattr": "true"})

        return self._get_csv(request_args=request_args,
                             return_dict=return_dict)

    def get_reports(self,
                    *args,
                    **kwargs):

        all_reports = list()

        for report_name in self.report_names:
            if report_name in self.report_with_retargeting:
                all_reports.append({report_name: self.get_report(api_report_name=report_name, *args, **kwargs)})
                all_reports.append({f"{report_name}_retargeting": self.get_report(api_report_name=report_name,
                                                                                  retargeting=True,
                                                                                  *args, **kwargs)})
            elif report_name in self.special_report_names:
                all_reports.append({report_name: self.get_report(api_report_name=report_name,
                                                                 different_additional_fields=True,
                                                                 *args, **kwargs)})
            else:
                all_reports.append({report_name: self.get_report(api_report_name=report_name, *args, **kwargs)})
        return all_reports


class TargetingValidationRulesReport(BaseAppsFlyer):

    additional_fields = ("rejected_reason", "rejected_reason_value",
                         "contributor1_match_type", "contributor2_match_type",
                         "contributor3_match_type", "match_type,device_category",
                         "gp_referrer", "gp_click_time", "gp_install_begin",
                         "amazon_aid", "keyword_match_type"
    )

    report_names = (
        'invalid_installs_report',
        'invalid_in_app_events_report'
    )

    def get_report(self,
                   from_date=None,
                   to_date=None,
                   timezone=DEFAULT_TIMEZONE,
                   api_report_name="invalid_installs_report",
                   return_dict=True
                   ):
        api_report_name, from_date, to_date = self.validate_dates_and_report_names(api_report_name,
                                                                                   self.report_names,
                                                                                   from_date,
                                                                                   to_date)
        self.api_report_name = api_report_name

        if not from_date or not to_date:
            from_date, to_date = self.get_default_dates()

        request_args = {"from": from_date,
                        "to": to_date,
                        "timezone": timezone,
                        "additional_fields": ",".join(self.additional_fields)}

        return self._get_csv(request_args=request_args,
                             return_dict=return_dict)

    def get_reports(self,
                    *args,
                    **kwargs):

        all_reports = list()

        for report_name in self.report_names:
            all_reports.append({report_name: self.get_report(api_report_name=report_name, *args, **kwargs)})

        return all_reports
