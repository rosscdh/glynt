# -*- coding: utf-8 -*-
import os
from django.conf import settings


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


def PUSHER_DATA(request):
    return {
        'PUSHER_APP_ID': getattr(settings, 'PUSHER_APP_ID'),
        'PUSHER_KEY': getattr(settings, 'PUSHER_KEY')
    }


def SESSION_PROJECT_UUID(request):
    """
    provides the current SESSION_PROJECT_UUID
    the session is set in glynt/middleware:LawpalCurrentProjectsMiddleware Service
    """
    return {
        'SESSION_PROJECT_UUID': request.session.get('current_project_uuid', None)
    }