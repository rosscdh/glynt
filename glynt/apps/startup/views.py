# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.contrib import messages
from django.core.urlresolvers import reverse

from services import EnsureFounderService
from forms import StartupProfileSetupForm, StartupAbridgedForm

from glynt.apps.utils import AjaxableResponseMixin
from glynt.apps.startup.bunches import StartupEngageLawyerBunch

import urlparse

import logging
logger = logging.getLogger('django.request')


class StartupProfileSetupView(FormView):
    form_class = StartupProfileSetupForm
    template_name = 'startup/profile-form.html'

    def get_success_url(self):
        messages.success(self.request, 'Thanks, your profile is complete.. now go find yourself a lawyer and get that funding')
        return reverse('startup:welcome')

    def get_context_data(self, **kwargs):
        context = super(StartupProfileSetupView, self).get_context_data(**kwargs)
        context.update({
            'founder': self.founder,
        })
        return context

    def get_form(self, form_class):
        """
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request}) # add the request to the form
        user = self.request.user

        founder_service = EnsureFounderService(user=user)
        self.founder = founder_service.process()
        # get the startup
        startup = self.founder.primary_startup

        kwargs.update({'initial': {
            'first_name': self.founder.user.first_name,
            'last_name': self.founder.user.last_name,
            'startup_name': startup.name,

            'photo': self.founder.photo,

            'website': startup.website,
            'summary': startup.summary,
            
            'already_incorporated': self.founder.data.get('already_incorporated', False),
            'already_raised_capital': self.founder.data.get('already_raised_capital', False),
            'process_raising_capital': self.founder.data.get('process_raising_capital', False),

            'incubator_or_accelerator_name': self.founder.data.get('incubator_or_accelerator_name'),

            'agree_tandc': self.founder.data.get('agree_tandc', False),
        }})
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        return super(StartupProfileSetupView, self).form_valid(form=form)


class StartupAbridgedView(FormView, AjaxableResponseMixin):
    form_class = StartupAbridgedForm
    template_name = 'startup/abridged-form.html'

    def get_form(self, form_class):
        """
        """
        kwargs = self.get_form_kwargs()

        kwargs.update({'request': self.request}) # add the request to the form
        user = self.request.user
        founder_service = EnsureFounderService(user=user)
        founder = founder_service.process()

        initial = StartupEngageLawyerBunch(founder=founder)

        kwargs.update({'initial': initial})
        return form_class(**kwargs)