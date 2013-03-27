import os
import sys

IS_TESTING = False
for test_app in ['jenkins','testserver','test']:
    if test_app in sys.argv[1:2]:
        IS_TESTING = True

SITE_ROOT = os.path.dirname(os.path.realpath(__file__+ '/../'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

gettext = lambda s: s

ADMINS = (
    ("Ross Crawford-dHeureuse", 'ross@lawpal.com'),
)

COMPRESSION_ENABLED = False

MANAGERS = ADMINS + (
    ("Alex Halliday", 'alex@lawpal.com'),
    ("Joe Musgrave", 'joe@lawpal.com'),
)

CMS_MODERATOR = ()

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

# Additional locations of static files
STATICFILES_DIRS = (
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

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'glynt.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'glynt.wsgi.application'

AUTHENTICATION_BACKENDS = (
'glynt.backends.EmailOrUsernameBackend',
'django.contrib.auth.backends.ModelBackend',
'socialregistration.contrib.facebook_js.auth.FacebookAuth',
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

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
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
    # Django CMS Helper app
    'public',

    # The default app that handles the basics
    'glynt.apps.default',
    # The Legal Firm App
    'glynt.apps.firm',
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
    # Remote and 3rd Party services (pdf/doc conversion)
    'glynt.apps.services',
)

CMS_APPS = (
    'cms',
    'mptt',
    'menus',
    'sekizai',

    'cms.plugins.link',
    'cms.plugins.picture',
    'cms.plugins.text',
)

HELPER_APPS = (
    'django_extensions',
    'templatetag_handlebars',
    'django_markdown',
    'socialregistration',
    'socialregistration.contrib.facebook_js',
    'djcelery',
    'bootstrap',
    # Userena
    'userena',
    'guardian',
    # Thumbnail generator
    'easy_thumbnails',
    # Activity stream
    'user_streams',
    'user_streams.backends.user_streams_single_table_backend',
    'django_markup',
    'compressor',
    'django_jenkins',

    # getsentry.com
    'raven.contrib.django.raven_compat',
)

# Handle south and its breaking tests
if IS_TESTING == True:
    # Log email to console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # disable celery for test
    BROKER_BACKEND = 'memory'

else:
    HELPER_APPS = HELPER_APPS + (
        'south',
    )


INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + CMS_APPS + HELPER_APPS


CMS_PERMISSION = False

CMS_TEMPLATES = (
    ('layout/base.html', 'Default (Bootstrap)'),
    ('layout/homepage.html', 'Homepage Template'),
    ('layout/default.html', 'Basic Template'),
    ('layout/document_list.html', 'Document List Template'),
    ('layout/new-home.html', '2.0 Homepage'),
    ('layout/lawyer-welcome.html', '2.0 Lawyer Welcome'),
    ('layout/lawyer-welcome-form.html', '2.0 Lawyer Form'),
    ('layout/twitter-test.html', 'Twitter Test')
)

CMS_APPHOOKS = ()

CMS_SHOW_START_DATE = True
CMS_SHOW_END_DATE = True

CMS_LANGUAGES = LANGUAGES = (
    ('en', gettext('English')),
)


USER_STREAMS_BACKEND = 'user_streams.backends.user_streams_single_table_backend.SingleTableDatabaseBackend'
USER_STREAMS_USE_UTC = True

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'client.ClientProfile' # our custom profile


USERENA_USE_MESSAGES = True
USERENA_LOGIN_AFTER_ACTIVATION = False # Enable beta style signup (manual activation)
USERENA_ACTIVATION_REDIRECT_URL = '/thanks-your-interest/'
USERENA_SIGNIN_REDIRECT_URL = '/'
USERENA_WITHOUT_USERNAMES = True # step userarena forcing user to provide username
USERENA_HIDE_EMAIL = True

FACEBOOK_API_KEY = '419217318130542'
FACEBOOK_SECRET_KEY = 'a8a6359a83c2af62c0aadb8e507bd15f'
FACEBOOK_REQUEST_PERMISSIONS = 'email,user_likes,user_about_me,read_stream'

LINKEDIN_CONSUMER_KEY = '1uh2ns1cn9tm'
LINKEDIN_CONSUMER_SECRET_KEY = 'MnrqdbtmM10gkz27'

LOGIN_REDIRECT_URL = '/client/'#/accounts/%(username)s/'
LOGIN_URL = '/client/login/'
LOGOUT_URL = '/social/logout/'

DATE_INPUT_FORMATS = ('%a, %d %b %Y', '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y',
'%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
'%B %d, %Y', '%d %B %Y', '%d %B, %Y')


COMPRESS_ENABLED = False
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



INTERNAL_IPS = ('127.0.0.1',)

# Custom test runner for this project
TEST_RUNNER = 'glynt.test_runner.GlyntAppTestRunner'
#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

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
        'console':{
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

HELLOSIGN_AUTH = ("", "")

DOCRAPTOR_KEY = "vIvrCmZtnQTC4p6V0k"

LAWPAL_PRIVATE_BETA = True


import djcelery
djcelery.setup_loader()

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
