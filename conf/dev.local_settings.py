# -*- coding: utf-8 -*-
LOCAL_SETTINGS = True
from settings import *

PROJECT_ENVIRONMENT = 'dev'

DEBUG = True
COMPRESSION_ENABLED = False

# For when running Debug = False
if DEBUG == False:
    # need to start http server in glynt/
    # cd root of glynt
    # python -mSimpleHTTPServer 8081
    # ./manage.py collectstatic
    MEDIA_URL = 'http://127.0.0.1:8081/media/'
    STATIC_URL = 'http://127.0.0.1:8081/static/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': './dev.db',

    }
}

CELERY_DEFAULT_QUEUE = 'lawpal-local'
BROKER_TRANSPORT_OPTIONS = {
    'region': 'eu-west-1',
}
CELERY_QUEUES = {
    CELERY_DEFAULT_QUEUE: {
        'exchange': CELERY_DEFAULT_QUEUE,
        'binding_key': CELERY_DEFAULT_QUEUE,
    }
}
BROKER_URL = 'sqs://{BROKER_USER}:{BROKER_PASSWORD}@sqs.eu-west-1.amazonaws.com/562971026743/{CELERY_DEFAULT_QUEUE}'.format(BROKER_USER=AWS_ACCESS_KEY_ID, BROKER_PASSWORD=AWS_SECRET_ACCESS_KEY, CELERY_DEFAULT_QUEUE=CELERY_DEFAULT_QUEUE)


GOOGLE_DISPLAY_NAME = 'LawPal.com - Development'
GOOGLE_OAUTH2_CLIENT_ID = '316492043888-ac8ngfmlkn9fapo9ovvvgng4esnujrvg.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'BjKXmFGh7d98zvowf9B31Bqv'
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.googleapis.com/auth/plus.me']

NEO4J_DATABASES = {
    'default' : {
        'HOST':'localhost',
        'PORT':7474,
        'ENDPOINT':'/db/data'
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200',
        'INDEX_NAME': 'dev-lawyers',
    },
    # 'firms': {
    #     'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
    #     'URL': 'http://127.0.0.1:9200',
    #     'INDEX_NAME': 'dev-firms',
    # },
}


# VERY IMPORTANT
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AWS_FILESTORE_BUCKET = 'local.lawpal.com'

FILEPICKER_API_KEY = 'A4Ly2eCpkR72XZVBKwJ06z'
CROCDOC_API_KEY = 'pRzHhZS4jaGes193db28cwyu'

PUSHER_APP_ID = 44301
PUSHER_KEY = '60281f610bbf5370aeaa'
PUSHER_SECRET = '72b185ac8ba23bda3552'

TWITTER_CONSUMER_KEY = 's4S1EAIeNded9aX5EBWwKQ'
TWITTER_CONSUMER_SECRET = 'GwkDznb11TzxHxQAsb5B5NbmzklpIlqpXcsXXB5sI'

if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + (
        # User switcher
        'debug_toolbar_user_panel',
        # Debug toolbar panels
        'template_timings_panel',
    )

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
        'debug_toolbar_user_panel.panels.UserPanel',
        'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    )

    if not IS_TESTING:
        MIDDLEWARE_CLASSES += (
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )
        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False
        }
        INSTALLED_APPS = INSTALLED_APPS + (
            'debug_toolbar',
        )


REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_AUTHENTICATION_CLASSES': (
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'PAGINATE_BY': 10,
}

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
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/tmp/lawpal-{env}.log'.format(env=PROJECT_ENVIRONMENT)
        }
    },
    'loggers': {
        'django.test': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'lawpal': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
