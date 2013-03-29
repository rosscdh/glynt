# -*- coding: utf-8 -*-

from django.utils import simplejson as json
from django.views.generic import FormView

from models import Lawyer
from forms import LawyerProfileSetupForm

import logging
logger = logging.getLogger('django.request')


class LawyerProfileSetupView(FormView):
    form_class = LawyerProfileSetupForm
    template_name = 'public/lawyer-profile-form.html'

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request}) # add the request to the form

        user = self.request.user
        try:
            lawyer_profile = user.lawyer_profile
        except:
            lawyer_profile = {}
            logger.info('A new Lawyer Profile is being created for user: %s' % user.username)

        kwargs.update({'initial': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }})
        return form_class(**kwargs)