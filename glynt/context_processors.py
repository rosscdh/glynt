# -*- coding: utf-8 -*-
from django.conf import settings
import os



def project_info(request):
    PROJECT_NAME = getattr(settings, 'PROJECT_NAME', 'LawPal')
    return {
      'PROJECT_NAME': PROJECT_NAME
    }


def project_environment(request):
    PROJECT_ENVIRONMENT = getattr(settings, 'PROJECT_ENVIRONMENT', 'prod')
    return {
      'PROJECT_ENVIRONMENT': PROJECT_ENVIRONMENT
    }


def default_profile_image(request):
    image = getattr(settings, 'DEFAULT_PROFILE_IMAGE', None)
    return {
        'default_profile_image': os.path.abspath('%s%s' % (settings.STATIC_URL, image))
    }

def USE_THREADEDCOMMENTS(request):
    return {
        'USE_THREADEDCOMMENTS': True if 'threadedcomments' in settings.INSTALLED_APPS else False
    }

def notification_unread(request):
    num_unread = 0
    if request.user.is_authenticated():
        num_unread = len(request.user.notifications.unread())
    return {
        'notification_unread': num_unread
    }