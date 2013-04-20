# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True
from settings import *

PROJECT_ENVIRONMENT = 'test'

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