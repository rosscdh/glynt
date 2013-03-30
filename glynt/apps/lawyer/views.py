# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.contrib import messages
from django.core.urlresolvers import reverse

from glynt.apps.lawyer.services import EnsureLawyerService

from forms import LawyerProfileSetupForm

import logging
logger = logging.getLogger('django.request')


class LawyerProfileSetupView(FormView):
    form_class = LawyerProfileSetupForm
    template_name = 'public/lawyer-profile-form.html'

    def get_success_url(self):
        return reverse('public:lawyer_setup_profile')

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request}) # add the request to the form

        user = self.request.user
        lawyer_service = EnsureLawyerService(user=user, firm_name=None, offices=[])
        lawyer_service.process()
        lawyer = lawyer_service.lawyer
        firm = lawyer_service.firm


        kwargs.update({'initial': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,

            'role': lawyer.role,
            'phone': lawyer.phone,

            'firm_name': getattr(firm, 'name', None),
            'practice_location_1': lawyer.data.get('practice_location_1', None),
            'practice_location_2': lawyer.data.get('practice_location_2', None),

            'years_practiced': lawyer.years_practiced,
            'profile_summary': lawyer.summary,
            'profile_bio': lawyer.bio,
            'agree_tandc': lawyer.data.get('agree_tandc', None),
        }})
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'You successfully updated your profile')
        return super(LawyerProfileSetupView, self).form_valid(form=form)