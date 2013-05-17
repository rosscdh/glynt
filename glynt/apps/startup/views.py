# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.contrib import messages
from django.core.urlresolvers import reverse

from services import EnsureFounderService
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

        founder_service = EnsureFounderService(founder_user=user)
        founder = founder_service.process()
        # get the startup
        startup = founder.primary_startup

        kwargs.update({'initial': {
            'first_name': founder.user.first_name,
            'last_name': founder.user.last_name,
            'startup_name': startup.name,
            
            'incubator_or_accelerator_name': founder.data.get('agree_tandc'),
            'already_raised_capital': founder.data.get('already_raised_capital'),
            'process_raising_capital': founder.data.get('process_raising_capital'),

            'incubator_or_accelerator_name': founder.data.get('incubator_or_accelerator_name'),

            'agree_tandc': founder.data.get('agree_tandc', False),
        }})
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        return super(StartupProfileSetupView, self).form_valid(form=form)