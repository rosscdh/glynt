# -*- coding: utf-8 -*-
from django.views.generic import DetailView, FormView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404

from glynt.apps.customer.services import EnsureCustomerService
from glynt.apps.customer.models import Customer

from forms import CustomerProfileSetupForm

import logging
logger = logging.getLogger('django.request')


class CustomerProfileSetupView(FormView):
    form_class = CustomerProfileSetupForm
    template_name = 'customer/profile-form.html'

    def get_success_url(self):
        messages.success(self.request, 'Success, you have updated your profile')
        return reverse('customer:welcome')

    def get_context_data(self, **kwargs):
        context = super(CustomerProfileSetupView, self).get_context_data(**kwargs)
        context.update({
            'customer': self.customer,
        })

        return context

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request})  # add the request to the form
        user = self.request.user

        customer_service = EnsureCustomerService(user=user)
        self.customer = customer_service.process()
        # get the startup
        startup = self.customer.primary_company

        kwargs.update({'initial': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.profile.phone,

            'photo': self.customer.photo,

            'company_name': startup.name,
            'website': startup.website,
            'summary': startup.summary,

            'agree_tandc': self.customer.data.get('agree_tandc', False),
        }})
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        return super(CustomerProfileSetupView, self).form_valid(form=form)


class CustomerProfileView(DetailView):
    model = Customer

    def get_object(self, queryset=None):
        """
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get(user=User.objects.get(username=slug))
        except ObjectDoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj