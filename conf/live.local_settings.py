# -*- coding: utf-8 -*-
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

SITE_ID = 1

DEBUG = False
TEMPLATE_DEBUG = DEBUG

USE_ETAGS = True

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATIC_ROOT = '/home/stard0g101/webapps/cartvine_static/'
MEDIA_ROOT = '/home/stard0g101/webapps/cartvine_static/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    '/home/stard0g101/webapps/cartvine_static/base/',
)

FACEBOOK_API_KEY = '238947626217872'
FACEBOOK_SECRET_KEY = '8a2b5757c513965faff0de2c35dcdbf2'