# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True
from settings import *

PROJECT_ENVIRONMENT = 'prod'

SITE_ID = 3

SECRET_KEY = 'g5ched^#zkyf!va9!2nwzzav3r@h8s+p%u2oeolg)@qak$!plc'

DEBUG = True
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lawpal_preview',
        'USER': 'postgres',
        'PASSWORD': 'p7vgff9h197gnres0kj13btoos4',
        'HOST': 'ec2-50-18-97-221.us-west-1.compute.amazonaws.com',
        'PORT': 5432
    },
    # 'heroku': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'd7c7vlhi6had88',
    #     'USER': 'u1uq45tflfbqqo',
    #     'PASSWORD': 'p7vgff9h197gnres0kj13btoos4',
    #     'HOST': 'ec2-54-225-205-183.compute-1.amazonaws.com',
    #     'PORT': 5642
    # }
}

TIME_ZONE = 'Europe/London'

USE_ETAGS = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATIC_ROOT = '/var/apps/preview-lawpal/static/'
MEDIA_ROOT = '/var/apps/preview-lawpal/media/'

ALLOWED_HOSTS = ['*']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'session_cache'
SESSION_COOKIE_SECURE = True


SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


# set the buck name: please note Name MUST NOT have . in it (SSL)
AWS_STORAGE_BUCKET_NAME = AWS_FILESTORE_BUCKET = 'preview-lawpal-com'

FILEPICKER_API_KEY = 'A4Ly2eCpkR72XZVBKwJ06z'
CROCDOC_API_KEY = 'GT9FRcpXVs61rgauSjCIzb3Y'


PUSHER_APP_ID = 44301
PUSHER_KEY = '60281f610bbf5370aeaa'
PUSHER_SECRET = '72b185ac8ba23bda3552'


GOOGLE_DISPLAY_NAME = 'LawPal.com - Development'
GOOGLE_OAUTH2_CLIENT_ID = '316492043888-mhcap930opo9uf2kj1rv9654odm6niqu.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'bigxopHAtqIPyWp4D6Lb-H0s'
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.googleapis.com/auth/plus.me']

FACEBOOK_API_KEY = '343632075713954'
FACEBOOK_SECRET_KEY = '4f9854b8fe8f5ccf27ac1ffcf5051b79'

LINKEDIN_CONSUMER_KEY = 'rrjwcpuvhfl1'
LINKEDIN_CONSUMER_SECRET = '2wm9DFbdUjLyi76U'


ANGEL_CLIENT_ID = 'c1602543cc137ebdf925cc8d63087bc5' # dev.lawpal.com
ANGEL_CLIENT_SECRET = '3b31b0e3b11d9d49dae7167035b4fe20' # dev.lawpal.com
ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email'}

TWITTER_CONSUMER_KEY = 'tr3Ei0ZIIbS2ZN31PkRHUA'
TWITTER_CONSUMER_SECRET = 'wfVTSbK3QZQFdGfCAChXtmhDe0Ictm7iRx6DD7UBio'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'lawpal'
EMAIL_HOST_PASSWORD = '0113633alex'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@lawpal.com'
SERVER_EMAIL = 'glynt@preview.lawpal.com'


RAVEN_CONFIG = {
    'dsn': 'https://b5a6429d03e2418cbe71cd5a4c9faca6:ddabb51af47546d1ac0e63cb453797ba@app.getsentry.com/6287',
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://giq8k0u0:8w1b1vt5lz38j3qo@fir-4141096.us-east-1.bonsai.io',
        'INDEX_NAME': 'glynt-preview',
    },
}
USE_ELASTICSEARCH = True


CELERY_DEFAULT_QUEUE = 'lawpal-preview'
BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-west-1',
}
CELERY_QUEUES = {
    CELERY_DEFAULT_QUEUE: {
        'exchange': CELERY_DEFAULT_QUEUE,
        'binding_key': CELERY_DEFAULT_QUEUE,
    }
}
BROKER_URL = 'sqs://{BROKER_USER}:{BROKER_PASSWORD}@sqs.eu-west-1.amazonaws.com/562971026743/{CELERY_DEFAULT_QUEUE}'.format(BROKER_USER=AWS_ACCESS_KEY_ID, BROKER_PASSWORD=AWS_SECRET_ACCESS_KEY, CELERY_DEFAULT_QUEUE=CELERY_DEFAULT_QUEUE)


SPLUNKSTORM_ENDPOINT = 'logs2.splunkstorm.com'
SPLUNKSTORM_PORT = 20824

#
# Abridge mailout service
#
ABRIDGE_ENABLED = True  # disabled by default
ABRIDGE_API_URL = 'https://abridge-preview.lawpal.com/'
ABRIDGE_PROJECT = 'lawpal-digest'

ABRIDGE_ACCESS_KEY_ID = 'd2cb78e5e9ccc2495c32'
ABRIDGE_SECRET_ACCESS_KEY = 'b2b42777c8953d99efb95e80722b3b76b956a7cd'
ABRIDGE_USERNAME = 'lawpal-preview'
ABRIDGE_PASSWORD = 'preview123'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        ('rest_framework.filters.DjangoFilterBackend',)
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'glynt.apps.api.v2_permissions.GlyntObjectPermission',
    ],
    'PAGINATE_BY': 10,
}

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
        'LOCATION': '/tmp/glynt.preview.cache',
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
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/lawpal-{env}.log'.format(env='preview'),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'logfile', 'splunkstorm'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'lawpal': {
            'handlers': ['splunkstorm', 'logfile', 'splunkstorm'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}