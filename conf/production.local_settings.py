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
LINKEDIN_CONSUMER_SECRET_KEY = '3eTYERhJZd4UJSjM'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'lawpal'
EMAIL_HOST_PASSWORD = '0113633alex'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'glynt@dev.weareml.com'
SERVER_EMAIL = 'glynt@dev.weareml.com'

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True