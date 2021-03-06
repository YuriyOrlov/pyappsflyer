import os
import environs

from platform import system

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.abspath(f'{BASE_DIR}/../')
PLATFORM = system()

# Environment variables, partly taken from .env
env = environs.Env()
try:
    environs.Env.read_env(BASE_DIR + '/../.env')
except IOError:
    pass

# AppsFlyer params
APP_FLYER_HOST = env.str('APP_FLYER_HOST', 'https://hq.appsflyer.com')
APP_FLYER_API_KEY = env.str('APP_FLYER_API_KEY', '')

DEFAULT_DAYS_NUMBER = env.int('DEFAULT_DAYS_NUMBER', 1)
DEFAULT_TIMEZONE = env.str('DEFAULT_TIMEZONE', 'Europe/Moscow')
DEFAULT_CSV_DELIMETER = env.str('DEFAULT_CSV_DELIMETER', ',')
DEFAULT_CSV_QUOTECHAR = env.str('DEFAULT_CSV_QUOTECHAR', '"')
DEFAULT_CSV_ENCODING = env.str('DEFAULT_CSV_ENCODING', "utf-8-sig")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s][%(threadName)s] %(funcName)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
