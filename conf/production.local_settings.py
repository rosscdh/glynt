# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True
from settings import *

PROJECT_ENVIRONMENT = 'prod'

SITE_ID = 4

DEBUG = False
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'd7c7vlhi6had88',
        'USER': 'u1uq45tflfbqqo',
        'PASSWORD': 'p7vgff9h197gnres0kj13btoos4',
        'HOST': 'ec2-54-225-205-183.compute-1.amazonaws.com',
        'PORT': 5642
    }
}

TIME_ZONE = 'Europe/London'

USE_ETAGS = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATIC_ROOT = '/var/apps/lawpal/static/'
MEDIA_ROOT = '/var/apps/lawpal/media/'

ALLOWED_HOSTS = ['*']

FACEBOOK_API_KEY = '343632075713954'
FACEBOOK_SECRET_KEY = '4f9854b8fe8f5ccf27ac1ffcf5051b79'

LINKEDIN_CONSUMER_KEY = 'gnesv6zvhzgn'
LINKEDIN_CONSUMER_SECRET = '3eTYERhJZd4UJSjM'
LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress']
LINKEDIN_EXTRA_FIELD_SELECTORS = ['email-address', 'headline', 'industry']
LINKEDIN_EXTRA_DATA = [('id', 'id'),
                       ('first-name', 'first_name'),
                       ('last-name', 'last_name'),
                       ('email-address', 'email_address'),
                       ('headline', 'headline'),
                       ('industry', 'industry')]


ANGEL_CLIENT_ID = '06aa0b726a71dc994bb44c3c4f3d9b91' # www.lawpal.com
ANGEL_CLIENT_SECRET = '26ea24f6107df875d2a410a8e2f55a27' # www.lawpal.com
ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email'}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'lawpal'
EMAIL_HOST_PASSWORD = '0113633alex'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'glynt@dev.weareml.com'
SERVER_EMAIL = 'glynt@dev.weareml.com'

HELLOSIGN_AUTH = ("sendrossemail@gmail.com", "zanshin77")


RAVEN_CONFIG = {
    'dsn': 'https://b5a6429d03e2418cbe71cd5a4c9faca6:ddabb51af47546d1ac0e63cb453797ba@app.getsentry.com/6287',
}

# Heroku - CloudAMQP
BROKER_URL = 'amqp://ixrhhdcu:PZffJcRS4NmILD65ss4s-aza7fKtTgYc@tiger.cloudamqp.com/ixrhhdcu'
BROKER_POOL_LIMIT = 1

SPLUNKSTORM_ENDPOINT = 'logs2.splunkstorm.com'
SPLUNKSTORM_PORT = 20824

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    },
    'fallback': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/glynt.cache',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'splunkstorm':{
            'level': 'INFO',
            'class': 'glynt.logger.SplunkStormLogger',
            'formatter': 'verbose'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['splunkstorm'],
            'level': 'INFO',
            'propagate': False,
        },
        'lawpal.services': {
            'handlers': ['splunkstorm'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}