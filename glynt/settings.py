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
)

NOTICEGROUP_EMAIL = (
 ("LawPal Tech", 'tech@lawpal.com'),
)

DEFAULT_FROM_EMAIL = 'noreply@localhost'
SERVER_EMAIL = 'glynt@localhost'

DATABASES = {
    'default': {
        'ENGINE': '', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ALLOWED_HOSTS = ['*']

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
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cusaaqg!ab^os!*+i*q9p8w4$%$)i93&(0ig%ts0nnjq5uj=*-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'glynt.middleware.LawpalSocialAuthExceptionMiddleware',
    'glynt.middleware.EnsureUserHasCompanyMiddleware',
    'glynt.middleware.LawpalCurrentProjectsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_filepicker.middleware.URLFileMapperMiddleware',
)


ROOT_URLCONF = 'glynt.urls'

# Needed for AngularJS
TASTYPIE_ALLOW_MISSING_SLASH = True

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'glynt.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.angel.AngelBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'glynt.backends.EmailOrUsernameBackend',
    #'userena.backends.UserenaAuthenticationBackend',
    #'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    #"django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    #"django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "glynt.context_processors.project_info",
    "glynt.context_processors.project_environment",
    "glynt.context_processors.default_profile_image",
    "glynt.context_processors.SESSION_PROJECT_UUID",
    "glynt.context_processors.PUSHER_DATA",
    "glynt.context_processors.USE_THREADEDCOMMENTS",
    "social_auth.context_processors.social_auth_by_type_backends",
    "social_auth.context_processors.social_auth_by_name_backends",
)

if DEBUG:
    TEMPLATE_CONTEXT_PROCESSORS += (
        "django.core.context_processors.debug",
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
    'django.contrib.formtools',
)

PROJECT_APPS = (
    # Public and Theme
    'public', # preferred
    # The inviter app
    'public.invite',
    # Older public site
    'glynt.apps.default',
    # The Api
    'glynt.apps.api',
    # The User Profile
    'glynt.apps.client',
    # The Customers
    'glynt.apps.customer',
    # The Companies
    'glynt.apps.company',
    # The Legal Firms
    'glynt.apps.firm',
    # The Lawyers
    'glynt.apps.lawyer',
    # Customer Projects
    'glynt.apps.project',
    # Company & Lawyer Transactions
    'glynt.apps.transact',
    # Checklist app
    'glynt.apps.todo',
    # Dashboard
    'glynt.apps.dashboard',
    # Services
    'glynt.apps.services',
    # Graph
    'glynt.apps.graph',
    # Crocdoc Helper
    'glynt.apps.crocdoc',
)

HELPER_APPS = (
    'guardian',
    'cicu',# image crop and upload
    'email_obfuscator',
    'django_extensions',
    'templatetag_handlebars',
    'django_markdown',

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
    'actstream',
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

    # Celery Tasks
    'djcelery',

    # Project System
    'fluent_comments',
    'threadedcomments',

    # Notications
    'notifications',

    # Abridge mailout
    'abridge',

    # feature switcher

    # user switcher
    'impersonate',

    # Object rules and permissions
    'rulez',

    # Api (v2)
    'rest_framework',
    'django_filters',

    # Haystack Search
    'haystack',
)


# Handle south and its breaking tests
if IS_TESTING == True:
    # Log email to console
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
    # disable celery for test
    BROKER_BACKEND = 'memory'
else:
    HELPER_APPS = HELPER_APPS + (
        # Db Migrations
        'south',
    )

# Process model updates in real time
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
USE_ELASTICSEARCH = True



# Primary installed apps goes here
# we do this so that we only test our apps
# the other apps will/can be tested seperately
INSTALLED_APPS = DJANGO_APPS + HELPER_APPS + PROJECT_APPS


# disable celery for test
BROKER_BACKEND = 'memory'

# comments app
COMMENTS_APP = 'fluent_comments'
FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = False # We handle our own email notifications

# notifications
NOTIFY_USE_JSONFIELD = True


LOGIN_URL          = '/start/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGIN_ERROR_URL    = '/login-error/'


HELLOSIGN_AUTH = ("sendrossemail@gmail.com", "test2007")

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'client.ClientProfile' # our custom profile


# Celery
BROKER_HEARTBEAT = 10 # helps with heroku connection limits
BROKER_CONNECTION_TIMEOUT = 3
BROKER_POOL_LIMIT = 1 # Very importnat for heroku, stops a max + 1 event
BROKER_CONNECTION_MAX_RETRIES = 2

# AWS
AWS_ACCESS_KEY_ID = 'AKIAI36HOWMVHPU4I3HA'
AWS_SECRET_ACCESS_KEY = '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'


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

FILEPICKER_API_KEY = None

FACEBOOK_API_KEY = '419217318130542'
FACEBOOK_SECRET_KEY = 'a8a6359a83c2af62c0aadb8e507bd15f'
FACEBOOK_REQUEST_PERMISSIONS = 'email,user_likes,user_about_me,read_stream'


LINKEDIN_CONSUMER_KEY = '1uh2ns1cn9tm'
LINKEDIN_CONSUMER_SECRET = 'MnrqdbtmM10gkz27'
LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress', 'r_network']
LINKEDIN_EXTRA_FIELD_SELECTORS = ['picture-url','email-address','current-status','headline','industry','summary']
LINKEDIN_EXTRA_DATA = [('id', 'id'),
                       ('first-name', 'first_name'),
                       ('last-name', 'last_name'),
                       ('email-address', 'email_address'),
                       ('headline', 'headline'),
                       ('industry', 'industry'),
                       ('summary', 'summary')]


ANGEL_CLIENT_ID = '00342c269e46c6059ab76013bb74ed44'
ANGEL_CLIENT_SECRET = '0f7ca41e548dcc04357984e5ceebfa26'
ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email'}

FULLCONTACT_API_KEY = '7280036b99dd362e'

TWITTER_CONSUMER_KEY = 'q4iigBXEJj7OBuIYHVF99g'
TWITTER_CONSUMER_SECRET = 'Ka9XGTeRlu1v7XRs2GSdK43Sd0l4j0eXXE2gI4iXd8E'

SOCIAL_AUTH_SLUGIFY_USERNAMES = True
SOCIAL_AUTH_UUID_LENGTH = 3 # greater than 0 otherwise it defaults to 3
SOCIAL_AUTH_BACKEND_ERROR_URL = '/'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ('first_name', 'last_name', 'full_name', 'email',)
SOCIAL_AUTH_PIPELINE = (
    'glynt.apps.client.pipeline.ensure_mutually_exclusive_userclass',
    'social_auth.backends.pipeline.social.social_auth_user',
    #'social_auth.backends.pipeline.associate.associate_by_email', # removed as we no longer need to provision poeple coming from preview.
    'glynt.apps.client.pipeline.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'glynt.apps.client.pipeline.ensure_user_setup',
    'glynt.apps.client.pipeline.profile_extra_details',
    #'glynt.apps.graph.pipeline.graph_user_connections',
)

POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_DISALLOW_COPIES_ON_REPLY = True
POSTMAN_DISABLE_USER_EMAILING = False
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_MAILER_APP = 'django.core.mail'

INTERCOM_API_SECRET = '-sjPyiyI5P44z3QsHLDUWfoLK8Rml7Wbg2wmj64L'


ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'project.project', 'project.projectlawyer', 'todo.todo', 'todo.attachment', 'threadedcomments.threadedcomment'),
    'MANAGER': 'glynt.apps.streams.LawpalStreamActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

DATE_INPUT_FORMATS = ('%a, %d %b %Y', '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y',
'%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
'%B %d, %Y', '%d %B %Y', '%d %B, %Y')


COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False

DEFAULT_MUGSHOT_URL = 'http://placehold.it/30x30'

# Signature Image generator
BLANK_SIG_IMAGE = os.path.join(STATIC_ROOT, 'signature/blank_sig.png'),
NO_SIG_IMAGE = os.path.join(STATIC_ROOT, 'signature/no_sig.png'),

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

CRISPY_TEMPLATE_PACK = 'crispy/bootstrap3'


#
# Abridge Integration
#
ABRIDGE_ENABLED = False  # disabled by default


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
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
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.AllowAny',
        'glynt.apps.api.v2_permissions.GlyntObjectPermission',
    ],
    'PAGINATE_BY': 10,
}

# Neat trick http://www.robgolding.com/blog/2010/05/03/extending-settings-variables-with-local_settings-py-in-django/
try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        print("Could not load local_settings")

if IS_TESTING:
    try:
        from test_settings import *
    except ImportError:
        print("Could not load test_settings")
