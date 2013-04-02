# -*- coding: utf-8 -*-
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

SITE_ID = 3

DEBUG = True
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

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATIC_ROOT = '/home/stard0g101/webapps/glynt_static/'
MEDIA_ROOT = '/home/stard0g101/webapps/glynt_static/media/'

# Additional locations of static files
STATICFILES_DIRS = ()

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


ANGEL_CLIENT_ID = '77339d6d557a0ae6c835baf89a22c2b0'
ANGEL_CLIENT_SECRET = '809bddbacb7dafbe482054bb96d944f4'
ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email message'}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'lawpal'
EMAIL_HOST_PASSWORD = '0113633alex'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'glynt@dev.weareml.com'
SERVER_EMAIL = 'glynt@dev.weareml.com'

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

HELLOSIGN_AUTH = ("sendrossemail@gmail.com", "zanshin77")

RAVEN_CONFIG = {
    'dsn': 'https://b5a6429d03e2418cbe71cd5a4c9faca6:ddabb51af47546d1ac0e63cb453797ba@app.getsentry.com/6287',
}

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
        }
    }
}