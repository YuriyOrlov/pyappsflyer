# PyAppsFlyer

Unofficial python erapper for AppsFlyer API.
https://www.appsflyer.com/
---

For working with this application you need to receive API_KEY in your
personal office on site.


#### Getting performance data report

---

```python
from pyappsflyer.api import PerformanceReport

report = PerformanceReport(api_key='your_api_key',
                           application_name="your_application_name",
    )
    
report.get_report()
```

Default report is partners report. If you wish to change and receive another:
```python
from pyappsflyer.api import PerformanceReport

report = PerformanceReport(api_key='your_api_key',
                           application_name="your_application_name",
    )
    
report.get_report('daily_report')
```
If report is not listed in available report you will be notified with an Exception.
All possible report are listed on application site. Please refer to them.

---
Report will be returned in python dict() type, so they can be easily transformed into JSON.

All method parameters:
---
* from_date - from what date to begin, date format - YYYY-MM-DD
* to_date - at what date to end, date format - YYYY-MM-DD
* timezone - timezone for api request, default - Europe/Moscow
* api_report_name - name of the performance report according to api documentation, string
* return_dict: return answer in dict or list, boolean

If you want to receive all possible reports, use another method.

```python
from pyappsflyer.api import PerformanceReport

report = PerformanceReport(api_key='your_api_key',
                           application_name="your_application_name",
    )
    
report.get_reports()
```
Reports will return in python list() type, so they can be easily transformed into JSON.


Also you could create an .env file with parameters shown below. The file must be near src
folder, or it would not be read. Do not put env file inside src folder.

Upon application start this file will be loaded and all additional parameters will be used.

APP_FLYER_HOST  - host of an AppsFlyer API.
APP_FLYER_API_KEY = AppsFlyer API KEY.

DEFAULT_DAYS_NUMBER = Number of days for timedelta. 
                      Application will try to receive all info for previous days, shown here. 
DEFAULT_TIMEZONE - default timezone is Europe/Moscow, could be changed. From API docs.
DEFAULT_CSV_DELIMETER - default csv files delimeter. From API docs.
DEFAULT_CSV_QUOTECHAR - default quotechar delimeter. From API docs.
DEFAULT_CSV_ENCODING - default encoding is UTF-8-SIG. From API docs.


If you want to receive other variants of reports there two classes.
RawDataReport and TargetingValidationRulesReport
These classes could be initialized as shown above. 



