# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ENVIRONMENT = 'prod'

IS_TESTING = False
for test_app in ['jenkins','testserver','test']:
    if test_app in sys.argv[1:2]:
        IS_TESTING = True

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

gettext = lambda s: s

COMPRESSION_ENABLED = False

ADMINS = (
    ("Ross Crawford-dHeureuse", 'ross@lawpal.com'),
)

MANAGERS = ADMINS + (
    ("Alex Halliday", 'alex@lawpal.com'),
    ("Joe Musgrave", 'joe@lawpal.com'),
)

NOTICEGROUP_EMAIL = (
 ("LawPal Tech", 'tech@lawpal.com'),   
)

DEFAULT_FROM_EMAIL = 'noreply@localhost'
SERVER_EMAIL = 'glynt@localhost'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'dev.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

if IS_TESTING:
    DATABASES['default']['TEST_NAME'] = '/tmp/testserver.db'

TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

PROJECT_NAME = 'LawPal'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

USE_ETAGS = True

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = '/m/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'

import djcelery
djcelery.setup_loader()

# Additional locations of static files
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i6=)1=4in#zyp&amp;g)^j2nl1abaeu)@2)^$ox5w7ac*uhml!uy-5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'glynt.middleware.LawpalSocialAuthExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'glynt.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'glynt.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.angel.AngelBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'glynt.backends.EmailOrUsernameBackend',
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "glynt.context_processors.project_info",
    "glynt.context_processors.project_environment",
    "glynt.context_processors.default_profile_image",
    "social_auth.context_processors.social_auth_by_type_backends",
    "social_auth.context_processors.social_auth_by_name_backends",
    "django.core.context_processors.request",
)

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DJANGO_APPS = (
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.humanize',
    'django.contrib.comments',
)

PROJECT_APPS = (
    # Public and Theme
    'public', # preferred
    # The inviter app
    'public.invite',
    # Older public site
    'glynt.apps.default', # depreciating @TODO end this


    # The Api
    'glynt.apps.api',
    # The Graph
    'glynt.apps.graph',
    # The Startups
    'glynt.apps.startup',
    # The Legal Firms
    'glynt.apps.firm',
    # The Lawyers
    'glynt.apps.lawyer',
    # Deals that have gone down
    'glynt.apps.deal',
    # Endorsements by users
    'glynt.apps.endorsement',
    # The Flyform
    'glynt.apps.flyform',
    # The primary document view system
    'glynt.apps.document',
    # The document authoring system
    'glynt.apps.author',
    # The End User - Client, those that consume the documents
    'glynt.apps.client',
    # The v2 Document Signing system
    'glynt.apps.smoothe',
    # The Document Signing system
    'glynt.apps.sign',
    # The Document Export system
    'glynt.apps.export',
    # Remote and 3rd Party services (pdf/doc conversion)
    'glynt.apps.services',
)

HELPER_APPS = (
    'menu',
    'cicu',# image crop and upload
    'django_extensions',
    'templatetag_handlebars',
    'django_markdown',
    # 'django_rq',
    'bootstrap',
    'crispy_forms',
    'django_markup',
    'compressor',
    # Social Authentication
    'social_auth',
    # User Profiles
    'userena',
    'guardian',
    # Thumbnail generator
    'easy_thumbnails',
    # Activity stream
    'user_streams',
    'user_streams.backends.user_streams_single_table_backend',
    # Cities
    'cities_light',
    # getsentry.com
    'raven.contrib.django.raven_compat',
    # jsonfields
    'jsonfield',
    # parsely
    'parsley',
    # clear-cache
    'clear_cache',
    # engless pagination
    'endless_pagination',
    # Search
    'haystack',
    # Celery Tasks
    'djcelery',
    # User switcher
    'debug_toolbar_user_panel',
)

# Handle south and its breaking tests
if IS_TESTING == True:
    # Log email to console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # disable celery for test
    BROKER_BACKEND = 'memory'

    HELPER_APPS = HELPER_APPS + (
        'django_jenkins',
    )
else:
    HELPER_APPS = HELPER_APPS + (
        'south',
    )


# Primary installed apps goes here
# we do this so that we only test our apps
# the other apps will/can be tested seperately
INSTALLED_APPS = DJANGO_APPS + HELPER_APPS + PROJECT_APPS 


LOGIN_URL          = '/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGIN_ERROR_URL    = '/login-error/'


USER_STREAMS_BACKEND = 'user_streams.backends.user_streams_single_table_backend.SingleTableDatabaseBackend'
USER_STREAMS_USE_UTC = True

HELLOSIGN_AUTH = ("sendrossemail@gmail.com", "test2007")

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'client.ClientProfile' # our custom profile


# Celery
BROKER_HEARTBEAT = 5 # helps with heroku connection limits
BROKER_POOL_LIMIT = 1 # Very importnat for heroku, stops a max + 1 event


USERENA_USE_MESSAGES = True
USERENA_LOGIN_AFTER_ACTIVATION = True # Enable beta style signup (manual activation)
USERENA_ACTIVATION_DAYS = 10
USERENA_ACTIVATION_REDIRECT_URL = '/'
USERENA_SIGNIN_REDIRECT_URL = '/'
USERENA_WITHOUT_USERNAMES = True # step userarena forcing user to provide username
USERENA_HIDE_EMAIL = True
USERENA_MUGSHOT_GRAVATAR = False
USERENA_MUGSHOT_DEFAULT = STATIC_URL +'img/default_avatar.png'

DEFAULT_PROFILE_IMAGE = '/img/default_avatar.png'

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
        'startup': {'size': (130, 60), 'crop': False},
    },
}


FACEBOOK_API_KEY = '419217318130542'
FACEBOOK_SECRET_KEY = 'a8a6359a83c2af62c0aadb8e507bd15f'
FACEBOOK_REQUEST_PERMISSIONS = 'email,user_likes,user_about_me,read_stream'


LINKEDIN_CONSUMER_KEY = '1uh2ns1cn9tm'
LINKEDIN_CONSUMER_SECRET = 'MnrqdbtmM10gkz27'
LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress', 'r_network']
LINKEDIN_EXTRA_FIELD_SELECTORS = ['picture-url','email-address', 'headline', 'industry']
LINKEDIN_EXTRA_DATA = [('id', 'id'),
                       ('first-name', 'first_name'),
                       ('last-name', 'last_name'),
                       ('email-address', 'email_address'),
                       ('headline', 'headline'),
                       ('industry', 'industry')]


ANGEL_CLIENT_ID = '00342c269e46c6059ab76013bb74ed44'
ANGEL_CLIENT_SECRET = '0f7ca41e548dcc04357984e5ceebfa26'
ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email'}

FULLCONTACT_API_KEY = '7280036b99dd362e'

TWITTER_CONSUMER_KEY = 'q4iigBXEJj7OBuIYHVF99g'
TWITTER_CONSUMER_SECRET = 'Ka9XGTeRlu1v7XRs2GSdK43Sd0l4j0eXXE2gI4iXd8E'

SOCIAL_AUTH_SLUGIFY_USERNAMES = True
SOCIAL_AUTH_UUID_LENGTH = 3 # greater than 0 otehrwise it defaults to 3
SOCIAL_AUTH_BACKEND_ERROR_URL = '/'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ('first_name', 'last_name', 'full_name', 'email',)
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email', # very insecure, only here to allow transfer of users from preview.lawpal
    'glynt.apps.graph.pipeline.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'glynt.apps.graph.pipeline.ensure_user_setup',
    'glynt.apps.graph.pipeline.profile_photo',
    'glynt.apps.graph.pipeline.graph_user_connections',
)

INTERCOM_API_SECRET = '-sjPyiyI5P44z3QsHLDUWfoLK8Rml7Wbg2wmj64L'


DATE_INPUT_FORMATS = ('%a, %d %b %Y', '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y',
'%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
'%B %d, %Y', '%d %B %Y', '%d %B, %Y')


COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False

if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + (
        'django.contrib.webdesign',
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

    if IS_TESTING:
        INSTALLED_APPS = INSTALLED_APPS + (
            'django_nose',
        )
        NOSE_ARGS = [
            '--with-coverage',
        ]

# Process model updates in real time
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
USE_ELASTICSEARCH = False

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
)

# Custom test runner for this project
TEST_RUNNER = 'glynt.test_runner.GlyntAppTestRunner'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.test': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'lawpal.services': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'lawpal.graph': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'lawpal.commands': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

DEFAULT_MUGSHOT_URL = 'http://placehold.it/30x30'

# Signature Image generator
BLANK_SIG_IMAGE = os.path.join(STATIC_ROOT, 'signature/blank_sig.png'),
NO_SIG_IMAGE = os.path.join(STATIC_ROOT, 'signature/no_sig.png'),

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

HELLOSIGN_AUTH = ("", "")

DOCRAPTOR_KEY = "vIvrCmZtnQTC4p6V0k"

LAWPAL_PRIVATE_BETA = True

ALLOWED_HOSTS = ['*']


# Neat trick http://www.robgolding.com/blog/2010/05/03/extending-settings-variables-with-local_settings-py-in-django/
if IS_TESTING:
    try:
        LOCAL_SETTINGS
    except NameError:
        try:
            from test_settings import *
        except ImportError:
            pass
else:
    try:
        LOCAL_SETTINGS
    except NameError:
        try:
            from local_settings import *
        except ImportError:
            pass
