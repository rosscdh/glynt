# -*- coding: utf-8 -*-
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

from django.contrib import messages
from django.shortcuts import redirect

from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import SocialAuthBaseException
from social_auth.utils import backend_setting, get_backend_name

SECURE_REQUIRED_PATHS = getattr(settings, 'SECURE_REQUIRED_PATHS', False)
HTTPS_SUPPORT = getattr(settings, 'HTTPS_SUPPORT', False)


class SSLRequiredMiddleware(object):
    def __init__(self):
        self.paths = SECURE_REQUIRED_PATHS
        self.enabled = self.paths and HTTPS_SUPPORT

    def process_request(self, request):
        if self.enabled and not request.is_secure():
            for path in self.paths:
                if request.get_full_path().startswith(path):
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'https://')
                    return HttpResponsePermanentRedirect(secure_url)
        return None


class LawpalSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    """ Custom override for social_auth exception middleware
    handles things like user account already linked etc"""
    def process_exception(self, request, exception):
        self.backend = self.get_backend(request, exception)
        if self.raise_exception(request, exception):
            return

        if isinstance(exception, SocialAuthBaseException):
            backend_name = get_backend_name(self.backend)
            message = self.get_message(request, exception)

            url = request.META.get('HTTP_REFERER', self.get_redirect_uri(request, exception))

            tags = ['social-auth']
            if backend_name:
                tags.append(backend_name)

            try:
                messages.error(request, message, extra_tags=' '.join(tags))
            except messages.MessageFailure:  # messages app is not installed
                url += ('?' in url and '&' or '?') + 'message=' + message
                if backend_name:
                    url += '&backend=' + backend_name
            return redirect(url)