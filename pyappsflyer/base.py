import logging
import csv
import requests

from typing import Optional
from logging.config import dictConfig
from contextlib import closing
from codecs import iterdecode
from datetime import datetime, timedelta
from furl import furl

from .settings import LOGGING, DEFAULT_DAYS_NUMBER,\
    DEFAULT_CSV_DELIMETER, DEFAULT_CSV_QUOTECHAR, DEFAULT_CSV_ENCODING,\
    APP_FLYER_HOST, APP_FLYER_API_KEY

dictConfig(LOGGING)

logger = logging.getLogger(__name__)


class BaseAppsFlyer:
    """
    Base class for AppsFlyer application.
    """

    def __init__(self,
                 application_name: str,
                 api_key: Optional[str] = None,
                 api_url: Optional[str] = None,
                 ):
        self.api_url = api_url or APP_FLYER_HOST
        self.api_action = 'export'
        self.application_name = application_name
        self.api_report_name = None
        self.api_version = 'v5'
        self.api_key = api_key or APP_FLYER_API_KEY

    def _prepare_url(self, **kwargs) -> furl:
        """
        Creates an url for ExpertSender using params provided in kwargs variable.
        :param kwargs: parameters to put as additional arguments into URL.
        :return:
        """
        if not self.api_key:
            raise Exception('API KEY not provided.')
        url = furl(self.api_url)
        url.path /= self.api_action
        url.path /= self.application_name
        url.path /= self.api_report_name
        url.path /= self.api_version
        url.args = {
            'api_token': self.api_key
        }

        if kwargs.get('request_args'):
            url.args.update(**kwargs['request_args'])

        return url

    def _validate_csv_request_answer(self, value):

        """
        Dirty hack because API is not return right status code
        :param value: value to check
        """

        if '<!DOCTYPE html>' in value:
            raise Exception('Error data received. Check API KEY')

    def _read_csv_file(self, reader, result):
        for num, record in enumerate(reader):
            if num == 0:
                self._validate_csv_request_answer(record)
            result.append(record)
        return result

    def _get(self, **kwargs):
        url = self._prepare_url(**kwargs)
        logger.debug(url)
        result = requests.request('GET', url.url)

        if result.status_code == 200:
            return result.json()
        logger.error(f"URL {url} |----| {result.content}")
        raise ConnectionError("Data was not received")

    def _get_csv(self,
                 delimeter=DEFAULT_CSV_DELIMETER,
                 quotechar=DEFAULT_CSV_QUOTECHAR,
                 encoding=DEFAULT_CSV_ENCODING,
                 **kwargs):
        url = self._prepare_url(**kwargs)
        logger.debug(url)
        result = list()

        try:
            with closing(requests.get(url.url, stream=True)) as receiver:
                if kwargs.get('return_dict'):
                    reader = csv.DictReader(iterdecode(receiver.iter_lines(),
                                                       encoding=encoding))
                else:
                    reader = csv.reader(iterdecode(receiver.iter_lines(),
                                                   encoding=encoding),
                                        delimiter=delimeter, quotechar=quotechar)

                result = self._read_csv_file(reader=reader,
                                             result=result)

        except Exception as err:
            logger.exception(err)

        return result

    def get_report(self):
        pass

    def get_reports(self):
        pass

    def validate_report_name(self, value, report_names):
        if value in report_names:
            return value
        raise Exception("No such report name in API documentation.")

    def validate_date_format(self, value):
        if not value:
            return None
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except (ValueError, TypeError) as err:
            logger.warning(err)
            return None

    def validate_dates_and_report_names(self,
                                        api_report_name,
                                        report_names,
                                        from_date,
                                        to_date):
        api_report_name = self.validate_report_name(api_report_name, report_names)

        from_date = self.validate_date_format(from_date)
        to_date = self.validate_date_format(to_date)

        return api_report_name, from_date, to_date

    def get_default_dates(self):
        from_date = (datetime.now() - timedelta(days=DEFAULT_DAYS_NUMBER)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        return from_date, to_date
