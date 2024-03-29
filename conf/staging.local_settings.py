# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True
from settings import *

PROJECT_ENVIRONMENT = 'staging'

SITE_ID = 3

SECRET_KEY = 'nbu+200^@(_o74_6st#!s=+1!@7gn7!8_mqbn&(+ci!f^s973+'

DEBUG = True
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'stard0g101_glynt',
        'USER': 'stard0g101_glynt',
        'PASSWORD': '1003507b',
        'HOST': 'web48.webfaction.com',
        # 'PORT': '',
    }
}

TIME_ZONE = 'Europe/London'

USE_ETAGS = True

MEDIA_URL = '/static/media/'

STATIC_URL = '/static/'

STATIC_ROOT = '/home/stard0g101/webapps/glynt_static/'
MEDIA_ROOT = '/home/stard0g101/webapps/glynt_static/media/'


GOOGLE_DISPLAY_NAME = 'LawPal.com - Development'
GOOGLE_OAUTH2_CLIENT_ID = '316492043888-ac8ngfmlkn9fapo9ovvvgng4esnujrvg.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'BjKXmFGh7d98zvowf9B31Bqv'
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.googleapis.com/auth/plus.me']

FACEBOOK_API_KEY = '343632075713954'
FACEBOOK_SECRET_KEY = '4f9854b8fe8f5ccf27ac1ffcf5051b79'

LINKEDIN_CONSUMER_KEY = 'gnesv6zvhzgn'
LINKEDIN_CONSUMER_SECRET = '3eTYERhJZd4UJSjM'


# ANGEL_CLIENT_ID = '06aa0b726a71dc994bb44c3c4f3d9b91' # www.lawpal.com
# ANGEL_CLIENT_SECRET = '26ea24f6107df875d2a410a8e2f55a27' # www.lawpal.com
ANGEL_CLIENT_ID = '77339d6d557a0ae6c835baf89a22c2b0' # dev.lawpal.com
ANGEL_CLIENT_SECRET = '8048545e591af07e18eef3049667decb' # dev.lawpal.com
ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email'}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'lawpal'
EMAIL_HOST_PASSWORD = '0113633alex'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'glynt@dev.weareml.com'
SERVER_EMAIL = 'glynt@dev.weareml.com'

ALLOWED_HOSTS = ['dev.lawpal.com']

RAVEN_CONFIG = {
    'dsn': 'https://b5a6429d03e2418cbe71cd5a4c9faca6:ddabb51af47546d1ac0e63cb453797ba@app.getsentry.com/6287',
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://jsy06hdx:km5ugyiy90yy17qg@banyan-8252692.us-east-1.bonsai.io',
        'INDEX_NAME': 'glynt-stage',
    },
}
USE_ELASTICSEARCH = True


# Heroku - CloudAMQP
#BROKER_URL = 'amqp://gxdzjcxo:sMKG0qU4bJlUWmRMkWKuArtPQiY3m84G@tiger.cloudamqp.com/gxdzjcxo'

SPLUNKSTORM_ENDPOINT = 'logs2.splunkstorm.com'
SPLUNKSTORM_PORT = 20824

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/home/stard0g101/memcached.sock'
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