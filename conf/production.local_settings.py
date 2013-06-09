# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True
from settings import *

PROJECT_ENVIRONMENT = 'prod'

SITE_ID = 4

SECRET_KEY = 'i6=)1=4in#zyp&amp;g)^j2nl1abaeu)@2)^$ox5w7ac*uhml!uy-5'

DEBUG = False
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'lawpal_production',
        'USER': 'postgres',
        'PASSWORD': 'p7vgff9h197gnres0kj13btoos4',
        'HOST': 'ec2-50-18-97-221.us-west-1.compute.amazonaws.com',
        'PORT': 5432
    }
}

TIME_ZONE = 'Europe/London'

USE_ETAGS = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATIC_ROOT = '/var/apps/lawpal/static/'
MEDIA_ROOT = '/var/apps/lawpal/media/'

ALLOWED_HOSTS = ['*']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'session_cache'
SESSION_COOKIE_SECURE = True


GOOGLE_DISPLAY_NAME = 'LawPal.com - Development'
GOOGLE_OAUTH2_CLIENT_ID = '316492043888-ac8ngfmlkn9fapo9ovvvgng4esnujrvg.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'BjKXmFGh7d98zvowf9B31Bqv'
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.googleapis.com/auth/plus.me']

FACEBOOK_API_KEY = '343632075713954'
FACEBOOK_SECRET_KEY = '4f9854b8fe8f5ccf27ac1ffcf5051b79'

LINKEDIN_CONSUMER_KEY = 'gnesv6zvhzgn'
LINKEDIN_CONSUMER_SECRET = '3eTYERhJZd4UJSjM'


ANGEL_CLIENT_ID = '06aa0b726a71dc994bb44c3c4f3d9b91' # www.lawpal.com
ANGEL_CLIENT_SECRET = '26ea24f6107df875d2a410a8e2f55a27' # www.lawpal.com
ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email'}

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'lawpal'
EMAIL_HOST_PASSWORD = '0113633alex'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@lawpal.com'
SERVER_EMAIL = 'glynt@lawpal.com'


RAVEN_CONFIG = {
    'dsn': 'https://b5a6429d03e2418cbe71cd5a4c9faca6:ddabb51af47546d1ac0e63cb453797ba@app.getsentry.com/6287',
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://giq8k0u0:8w1b1vt5lz38j3qo@fir-4141096.us-east-1.bonsai.io',
        'INDEX_NAME': 'glynt-prod',
    },
}
USE_ELASTICSEARCH = True


# Heroku - CloudAMQP
#BROKER_URL = 'amqp://gqhezwgc:1JylV9VKTXnlA9iuy9WFqIOqbl4yTmQa@tiger.cloudamqp.com/gqhezwgc'

SPLUNKSTORM_ENDPOINT = 'logs2.splunkstorm.com'
SPLUNKSTORM_PORT = 20824

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    },
    'session_cache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 3600
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
        },
        'lawpal.graph': {
            'handlers': ['splunkstorm'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}