import os
import logging
import csv
import json
import requests

from datetime import datetime as dt
from datetime import timedelta as tdl
from datetime import date
from typing import Optional, Union, List, Tuple
from uuid import uuid4
from contextlib import closing
from codecs import iterdecode
from furl import furl

from .settings import DEFAULT_DAYS_NUMBER,\
    DEFAULT_CSV_DELIMETER, DEFAULT_CSV_QUOTECHAR, DEFAULT_CSV_ENCODING,\
    APP_FLYER_HOST, APP_FLYER_API_KEY, FILES_DIR, PLATFORM

from .exceptions import PyAFValidationError,\
    PyAFCommunicationError, PyAFUnknownError,\
    AuthenticationError, PyAFProcessingError


def get_random_filename(filename: str = None,
                        folder: str = None,
                        add_current_date: bool = True,
                        ext: str = 'csv',
                        possible_ext: Tuple[str] = ('csv', 'json')
                        ) -> str:
    """
    Function returns full path for saving file.

    :param filename: an old filename if provided, else there will be an UUID4 as a filenamename
           default: None
    :param folder: path to a folder, else the base folder will be used
           default: None
    :param add_current_date: current YYYY/MM/DD will be added as a folder, if needed
           default: True
    :param ext: file extension with which to save
    :param possible_ext: possible file extensions
    :return:
    """
    if ext not in possible_ext:
        ext = 'csv'

    # "Date as folder" delimiter according to the current user's system
    plt_folder_delimiter = {
        'Windows': '\\',
        'Linux': '/'
    }

    if filename:
        filename, _ = os.path.splitext(filename)
        filename = f"{filename}.{ext}"
    else:
        filename = f"{str(uuid4())}.{ext}"

    components = []
    if folder:
        components.append(f'{FILES_DIR}{plt_folder_delimiter.get(PLATFORM)}{folder}')
    else:
        components.append(FILES_DIR)

    if add_current_date:
        str_date = f"%Y{plt_folder_delimiter.get(PLATFORM, '/')}%m{plt_folder_delimiter.get(PLATFORM, '/')}%d"
        components.append(date.today().strftime(str_date))
    components.append(filename)

    return os.path.join(*components)


class BaseAppsFlyer:
    """
    Base class for AppsFlyer application.
    """

    __slots__ = ('logger', 'api_url', 'api_action',
                 'application_name', 'api_report_name',
                 'api_version', 'api_key')

    def __init__(self,
                 application_name: str,
                 api_key: Optional[str] = None,
                 api_url: Optional[str] = None,
                 ):
        self.logger = logging.getLogger(application_name)
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
        :return: furl instance with prepared URL
        """
        if not self.api_key:
            raise AuthenticationError('API KEY not provided.')
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

    def _read_csv_file(self,
                       reader: Union[csv.reader, csv.DictReader],
                       result: list) -> list:
        """
        Method reads CSV file, checks if something present in request answer
        and returns parsed data.

        :param reader: file reader
        :param result: result for elements in file
        :return: list of records
        """

        for num, record in enumerate(reader):
            if num == 0:
                # Checks the first row if there no problem in request answer
                # because AppsFlyer could answer with 200 OK and without any CSV data.
                self.validate_csv_request_answer(record)
            result.append(record)
        return result

    def _get(self, **kwargs) -> json:
        """
        Method receives result from AppsFlyer

        :param kwargs: additional params for an URL
        :return: result in JSON format
        """
        url = self._prepare_url(**kwargs)
        self.logger.debug(url)
        result = requests.request('GET', url.url)

        if result.status_code == 200:
            return result.json()
        self.logger.error(f"URL {url} |----| {result.content}")
        raise PyAFCommunicationError("Data was not received")

    def _get_csv(self,
                 encoding=DEFAULT_CSV_ENCODING,
                 **kwargs) -> list:
        """
        Method receives CSV file in a stream parses it and passes further.
        If there is a need to save those files in CSV or JSON it saves them
        :param encoding: CSV encoding
               default: utf-8-sig
        :param kwargs: additional params for adding something in request URL
                       or if CSV must return reader as a dict and not as row by row.
        """
        url = self._prepare_url(**kwargs)
        self.logger.debug(url)
        filename = get_random_filename(folder='received_files')
        result = []

        try:
            # Reads all stream from AppsFlyer API
            with closing(requests.get(url.url, stream=True)) as receiver:
                reader = csv.DictReader(iterdecode(receiver.iter_lines(),
                                                   encoding=encoding))
                # Converts received CSV into list
                result = self._read_csv_file(reader=reader, result=result)

            if kwargs.get('to_csv'):
                self.write_file(result, filename)
            elif kwargs.get('to_json'):
                self.write_file(result, filename, 'json')

        except Exception as err:
            raise PyAFProcessingError(
                'Error while processing file'
            ) from err
        finally:
            return result

    def get_report(self):
        """
        Main method for receiving reports.
        """
        try:
            self._get_report()
        except Exception as err:
            raise PyAFUnknownError(
                'Unknown error'
            ) from err

    def _get_report(self):
        """
        Method to be reassgned in child classes.
        :return:
        """
        pass

    def get_reports(self):
        pass

    def validate_date_format(self, value: str) -> None:
        """
        Method checks id data format is invalid.

        :param value: date as a string
        """
        try:
            dt.strptime(value, "%Y-%m-%d")
        except ValueError as err:
            raise PyAFValidationError(
                'Date format is invalid'
            ) from err
        except TypeError:
            self.logger.info('Date not set')

    def validate_dates_and_report_names(self,
                                        api_report_name: str,
                                        allowed_report_names: List[str],
                                        from_date: str,
                                        to_date: str) -> None:
        """
        Method validates date formats and report names.
        If something is wrong, than exception will be raised.

        :param api_report_name: report name to be used in API query
        :param allowed_report_names: list of an allowed report names
        :param from_date: date in string format
        :param to_date: date in string format
        """
        self.validate_report_name(api_report_name, allowed_report_names)
        self.validate_date_format(from_date)
        self.validate_date_format(to_date)

    @staticmethod
    def get_default_dates() -> Tuple[str, str]:
        """
        Method returns default values for dates if no dates were transferred.
        :return: tuple with two dates
        """
        from_date = (dt.now() - tdl(days=DEFAULT_DAYS_NUMBER)).strftime("%Y-%m-%d")
        to_date = dt.now().strftime("%Y-%m-%d")
        return from_date, to_date

    @staticmethod
    def do_reports_exclusion(report_names: List[str], exclude_reports: Tuple[str]) -> List[str]:
        """
        Reports to be excluded, if they are not needed in query to an AppsFlyer API.

        :param report_names: default report names to be used in query
        :param exclude_reports: report names, which must be excluded
        :return: an array of strings with report names
        """
        return [
            report_name for report_name in report_names
            if report_name not in exclude_reports
        ]

    @staticmethod
    def validate_report_name(value, report_names: List[str]) -> List[str]:
        """
        Method validates that such report is in reports list
        which user could receive.
        :param value: report name
        :param report_names: allowed reports
        :return: report name
        """

        if value in report_names:
            return value
        raise PyAFValidationError("No such report name in API documentation.")

    @staticmethod
    def validate_csv_request_answer(value: str) -> None:
        """
        Hack, because API is not return right status code
        :param value: value to check
        """

        if '<!DOCTYPE html>' in value:
            raise PyAFValidationError('Error data received. Check API KEY')

    @staticmethod
    def write_file(result: List[str], filename: str, extension: str ='csv') -> None:
        """
        Method saves a file in CSV or JSON if needed.

        :param result: elements extracted from stream
        :param filename: file name
        :param extension: file's extension
        """
        with open(filename, 'w+') as file:
            if extension == 'json':
                json.dump(result, file)
            else:
                writer = csv.writer(file)
                for record in result:
                    writer.writerow(record)
