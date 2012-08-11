# -*- coding: utf-8 -*-
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

SITE_ID = 2

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

USE_ETAGS = True

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATIC_ROOT = '/home/stard0g101/webapps/cartvine_static/'
MEDIA_ROOT = '/home/stard0g101/webapps/cartvine_static/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    '/home/stard0g101/webapps/cartvine_static/base/',
)

FACEBOOK_API_KEY = '343632075713954'
FACEBOOK_SECRET_KEY = '4f9854b8fe8f5ccf27ac1ffcf5051b79'

LINKEDIN_CONSUMER_KEY = 'gnesv6zvhzgn'
LINKEDIN_CONSUMER_SECRET_KEY = '3eTYERhJZd4UJSjM'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'glynt'
EMAIL_HOST_PASSWORD = 'test2007'
DEFAULT_FROM_EMAIL = 'glynt@dev.weareml.com'
SERVER_EMAIL = 'glynt@dev.weareml.com'
# EMAIL_PORT = ''
# EMAIL_USE_TLS = ''