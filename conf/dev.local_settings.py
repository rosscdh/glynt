LOCAL_SETTINGS = True
from settings import *

PROJECT_ENVIRONMENT = 'dev'

# VERY IMPORTANT
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'lawpal.services': {
            'handlers': ['splunkstorm'],
            'level': 'INFO',
            'propagate': False,
        },
        'lawpal.graph': {
            'handlers': ['splunkstorm'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}


TWITTER_CONSUMER_KEY = 's4S1EAIeNded9aX5EBWwKQ'
TWITTER_CONSUMER_SECRET = 'GwkDznb11TzxHxQAsb5B5NbmzklpIlqpXcsXXB5sI'
