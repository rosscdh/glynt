# -*- coding: utf-8 -*-
from django.conf import settings

from django.contrib import messages
from django.shortcuts import redirect

from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import SocialAuthBaseException
from social_auth.utils import backend_setting, get_backend_name


class LawpalSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    """ Custom override for social_auth exception middleware
    handles things like user account already linked etc"""
    def process_exception(self, request, exception):
        self.backend = self.get_backend(request, exception)

        # if self.raise_exception(request, exception):
        #     return

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