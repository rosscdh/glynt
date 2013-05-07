# -*- coding: utf-8 -*-
from django.conf import settings
import os
import hmac, hashlib


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


def intercomio_userhash(request):
    intercom_unique_hash = None
    if request.user.is_authenticated():
        intercom_unique_hash = hmac.new(settings.INTERCOM_API_SECRET, str(request.user.pk), digestmod=hashlib.sha256).hexdigest()

    return {
        'intercomio_userhash': intercom_unique_hash
    }
