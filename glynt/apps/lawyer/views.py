# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from glynt.apps.lawyer.services import EnsureLawyerService

from forms import LawyerProfileSetupForm

import logging
logger = logging.getLogger('django.request')


class LawyerProfileSetupView(FormView):
    form_class = LawyerProfileSetupForm
    template_name = 'lawyer/profile-form.html'

    def get_success_url(self):
        return reverse('lawyer:thanks')

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request}) # add the request to the form

        user = self.request.user
        lawyer_service = EnsureLawyerService(user=user)
        lawyer_service.process()
        lawyer = lawyer_service.lawyer
        firm = lawyer_service.firm

        volume_incorp_setup = json.dumps(lawyer.data.get('volume_incorp_setup', {}))
        volume_seed_financing = json.dumps(lawyer.data.get('volume_seed_financing', {}))
        volume_series_a = json.dumps(lawyer.data.get('volume_series_a', {}))

        kwargs.update({'initial': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,

            'position': lawyer.data.get('position', None),
            'phone': lawyer.phone,

            'firm_name': getattr(firm, 'name', None),
            'practice_location_1': lawyer.data.get('practice_location_1', None),
            'practice_location_2': lawyer.data.get('practice_location_2', None),

            'years_practiced': lawyer.years_practiced,
            'summary': lawyer.summary,
            'bio': lawyer.bio,
            'if_i_wasnt_a_lawyer': lawyer.data.get('if_i_wasnt_a_lawyer', None),

            'photo': lawyer.photo,

            'volume_incorp_setup': volume_incorp_setup,
            'volume_seed_financing': volume_seed_financing,
            'volume_series_a': volume_series_a,

            'agree_tandc': lawyer.data.get('agree_tandc', None),
        }})
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'You successfully updated your profile')
        form.delete_cookie()
        return super(LawyerProfileSetupView, self).form_valid(form=form)