import pytest
import logging

from os import path
from logging.config import dictConfig

CURRENT_DIR = path.dirname(__file__)


def full_path(file: str) -> str:
    return path.join(CURRENT_DIR, file)


@pytest.fixture(scope='session', autouse=True)
def set_base_test_logger():
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            'console': {
                'handlers': ['console'],
                'propagate': False}
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }

    dictConfig(LOGGING)
