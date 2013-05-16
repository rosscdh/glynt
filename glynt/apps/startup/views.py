# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.contrib import messages
from django.core.urlresolvers import reverse

from services import EnsureFounderService, EnsureStartupService
from forms import StartupProfileSetupForm

import urlparse

import logging
logger = logging.getLogger('django.request')


class StartupProfileSetupView(FormView):
    form_class = StartupProfileSetupForm
    template_name = 'startup/profile-form.html'

    def get_success_url(self):
        messages.success(self.request, 'Thanks, your profile is complete.. now go find yourself a lawyer and get that funding')
        return reverse('startup:welcome')

    def get_form(self, form_class):
        """
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request}) # add the request to the form
        user = self.request.user

        founder_service = EnsureFounderService(user=user)
        founder = founder_service.process()
        # if founder:
        #     startup_service = EnsureStartupService(founder=founder)
        #     startup = startup_service.process()

        kwargs.update({'initial': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'agree_tandc': None,
        }})
        return form_class(**kwargs)