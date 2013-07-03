# -*- coding: utf-8 -*-
from django.views.generic import DetailView, CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import Http404

from glynt.apps.utils import AjaxableResponseMixin

from glynt.apps.customer.services import EnsureCustomerService
from glynt.apps.customer.models import Customer

import logging
logger = logging.getLogger('django.request')


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


class CreateCustomerView(AjaxableResponseMixin, CreateView):
    model = Customer
    http_method_names = [u'post']

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST
            first_name = data.__getitem__('customers-first_name')
            last_name = data.__getitem__('customers-last_name')
            user_name = "%s-%s" % (first_name, last_name)
            user_email = data.__getitem__('customers-email')
            user, is_new = User.objects.get_or_create(email=user_email, defaults={'username': user_name, 'first_name': first_name, 'last_name': last_name})
            customer = EnsureCustomerService(user=user)
            customer.process()

            # Save form to new customer data
            return self.render_to_json_response({'message': "Customer saved", 'status': 200})
