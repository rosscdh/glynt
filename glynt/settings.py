import os
import sys

IS_TESTING = False
for test_app in ['jenkins','testserver','test']:
    if test_app in sys.argv[1:2]:
     IS_TESTING = True

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ("Ross Crawford-d'Heureuse", 'ross@lawpal.com'),
)
COMPRESSION_ENABLED = False
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'dev.db'),
        #'NAME': '/tmp/testserver.db',
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

if not IS_TESTING:
    SITE_ID = 1
else:
    SITE_ID = 3

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

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(STATIC_ROOT, 'base'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i6=)1=4in#zyp&amp;g)^j2nl1abaeu)@2)^$ox5w7ac*uhml!uy-5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'glynt.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'glynt.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'glynt.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
    'socialregistration.contrib.facebook_js.auth.FacebookAuth',
    #'socialregistration.contrib.linkedin.auth.LinkedInAuth',
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
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
"socialregistration.contrib.facebook_js.context_processors.FacebookTemplateVars",
"glynt.context_processors.project_info",
)

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DJANGO_APPS = (
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
    # The default app that handles the basics
    'glynt.apps.default',
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
    # The Api
    'glynt.apps.api',
)

HELPER_APPS = (
    'django_extensions',
    'templatetag_handlebars',
    'django_markdown',
    'taggit',
    'django_jenkins',
    'categories',
    'categories.editor',
    'mptt',
    'django_xhtml2pdf',
    'socialregistration',
    'socialregistration.contrib.facebook_js',
    #'socialregistration.contrib.linkedin_js',
    'djcelery',
    'bootstrap',
    # Userena
    'userena',
    'guardian',
    'easy_thumbnails',
    'user_streams',
    'user_streams.backends.user_streams_single_table_backend',
    'django_comments_xtd',
    'django_markup',
    'compressor',
    'tastypie_elasticsearch',
)

ES_INDEX_SERVER = 'http://127.0.0.1:9200/'

# Handle south and its breaking tests
if not IS_TESTING:
    HELPER_APPS = HELPER_APPS + ('south',)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + HELPER_APPS

USER_STREAMS_BACKEND = 'user_streams.backends.user_streams_single_table_backend.SingleTableDatabaseBackend'
USER_STREAMS_USE_UTC = True

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'client.ClientProfile'
USERENA_WITHOUT_USERNAMES = True
USERENA_HIDE_EMAIL = True

FACEBOOK_API_KEY = '419217318130542'
FACEBOOK_SECRET_KEY = 'a8a6359a83c2af62c0aadb8e507bd15f'
FACEBOOK_REQUEST_PERMISSIONS = 'email,user_likes,user_about_me,read_stream'

LINKEDIN_CONSUMER_KEY = '1uh2ns1cn9tm'
LINKEDIN_CONSUMER_SECRET_KEY = 'MnrqdbtmM10gkz27'

# LOGIN_REDIRECT_URL = '/'
# LOGOUT_URL = '/social/logout/'
LOGIN_REDIRECT_URL = '/client/'#/accounts/%(username)s/'
LOGIN_URL = '/client/login/'
LOGOUT_URL = '/social/logout/'

COMMENTS_XTD_CONFIRM_EMAIL = False
#COMMENTS_APP = 'django_comments_xtd'

DATE_INPUT_FORMATS = ('%a, %d %b %Y', '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y',
'%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
'%B %d, %Y', '%d %B %Y', '%d %B, %Y')

CATEGORIES_SETTINGS = {
    'ALLOW_SLUG_CHANGE': False,
    'CACHE_VIEW_LENGTH': 0,
    'RELATION_MODELS': ["document.DocumentTemplateCategory"],
    'M2M_REGISTRY': {},
    'FK_REGISTRY': {},
    'THUMBNAIL_UPLOAD_PATH': 'uploads/categories/thumbnails',
    'THUMBNAIL_STORAGE': 'django.core.files.storage.FileSystemStorage',
    'SLUG_TRANSLITERATOR': lambda x: x,
}

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

if DEBUG:
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

    INSTALLED_APPS = INSTALLED_APPS + (
    'django.contrib.webdesign',
    )

INTERNAL_IPS = ('127.0.0.1',)

# Custom test runner for this project
TEST_RUNNER = 'glynt.test_runner.GlyntAppTestRunner'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Signature Image generator
BLANK_SIG_IMAGE = os.path.join(STATIC_ROOT, 'signature/blank_sig.png'),
NO_SIG_IMAGE = os.path.join(STATIC_ROOT, 'signature/no_sig.png'),

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'
TEMPLATED_EMAIL_DJANGO_SUBJECTS = {
    'invite_to_sign': 'You have been invited to sign',
}

BROKER_URL = 'amqp://guest:guest@localhost:5672/'


import djcelery
djcelery.setup_loader()

try:
    from local_settings import *
except ImportError:
    pass
