# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from glynt.apps.project.services.project_service import VisibleProjectsService
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import SocialAuthBaseException
from social_auth.utils import get_backend_name


class EnsureUserHasCompanyMiddleware(object):
    """ if the user is a is_customer
    and has no company then get them to complete the signup form
    """
    def process_request(self, request):
        if request.user.is_authenticated():

            if request.user.profile.is_customer:

                try:
                    request.user.companies.all()[0]

                except IndexError:
                    signup_url = reverse('client:confirm_signup', kwargs={'slug': request.user.username})
                    logout_url = reverse('logout')

                    if request.get_full_path() not in [signup_url, logout_url]:
                        return redirect(signup_url)
        return None


class LawpalSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    """ Custom override for social_auth exception middleware
    handles things like user account already linked etc"""
    def process_exception(self, request, exception):
        self.backend = self.get_backend(request, exception)

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


class LawpalCurrentProjectsMiddleware(object):
    """
    Middleware to ensure that the template has access to the
    {
        projects: [Project, Project], # relative to customer or lawyer user_class
        project: Project,
    }
    object
    """
    def process_request(self, request):
        projects_service = VisibleProjectsService(request=request)

        request.projects, request.project = projects_service.get()

        return None