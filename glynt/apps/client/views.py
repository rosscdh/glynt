# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User


from forms import ConfirmLoginDetailsForm

import logging
logger = logging.getLogger('django.request')


class ConfirmLoginDetailsView(UpdateView):
    model = User
    slug_field = 'username'
    template_name = 'client/confirm_login_details.html'
    form_class = ConfirmLoginDetailsForm

    def get_success_url(self):
        """ redirect to homepage, which is where the logic for user_class
        is applied """
        return reverse('public:homepage')

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        user = self.request.user
        customer = self.request.user.customer_profile
        kwargs.update({
            'request': self.request,
            'initial': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'company_name': customer.company_name,
                'phone': customer.phone
            }
        })
        return form_class(**kwargs)

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        slug_field = self.get_slug_field()
        queryset = User.objects.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            form.save()
            logger.info('User %s has confirmed their account' % request.user)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
