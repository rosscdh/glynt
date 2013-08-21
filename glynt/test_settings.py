# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True
from settings import *

import hashlib
import random

# Custom test runner for this project
TEST_RUNNER = 'glynt.test_runner.GlyntAppTestRunner'

PROJECT_ENVIRONMENT = 'test'

INSTALLED_APPS = INSTALLED_APPS + (
    'django_nose',
)
NOSE_ARGS = [
    #'--with-coverage',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.test': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.test.behave': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'ERROR',
            'propagate': True,
        },
        'lawpal.services': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'lawpal.graph': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'lawpal.commands': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

def AutoSlugFieldGenerator():
    hash_val = '{r}'.format(r=random.random())
    h = hashlib.sha1(hash_val)
    return h.hexdigest()

MOMMY_CUSTOM_FIELDS_GEN = {
    'autoslug.fields.AutoSlugField': AutoSlugFieldGenerator,
}
