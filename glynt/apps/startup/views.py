# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.contrib import messages
from django.core.urlresolvers import reverse

from models import Founder, Startup
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
