# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True
from settings import *

import hashlib
import random

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
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.test.behave': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'lawpal.services': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'lawpal.graph': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'lawpal.commands': {
            'handlers': ['console'],
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
