# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import DetailView, FormView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404

from glynt.apps.customer.services import EnsureCustomerService
from glynt.apps.customer.models import Customer
from glynt.apps.project.models import Project

from .forms import CustomerProfileSetupForm

import logging
logger = logging.getLogger('django.request')


class CustomerLoginLogic(object):
    """ Login logic used to determin what to show """
    user = None
    customer = None

    def __init__(self, user):
        self.user = user
        try:
            self.customer = self.user.customer_profile
        except ObjectDoesNotExist:
            self.customer = None
            logger.error("founder profile not found for %s" % self.user)

    @property
    def url(self):
        num_projects = Project.objects.filter(customer=self.customer).count()

        if num_projects > 0:
            return reverse('dashboard:overview')
        else:
            return reverse('project:create')

    def redirect(self):
        return redirect(self.url)


class CustomerRequiredViewMixin(object):
    """
    Mixin to ensure that only a lawyer user
    can view this view
    """
    @method_decorator(user_passes_test(lambda u: u.profile.is_customer))
    def dispatch(self, *args, **kwargs):
        return super(CustomerRequiredViewMixin, self).dispatch(*args, **kwargs)


class CustomerProfileSetupView(CustomerRequiredViewMixin, FormView):
    form_class = CustomerProfileSetupForm
    template_name = 'customer/profile-form.html'

    def get_success_url(self):
        messages.success(self.request, 'Success, you have updated your profile')
        return reverse('public:homepage')

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
            'phone': self.customer.phone,

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
