# -*- coding: utf-8 -*-
from django.views.generic import DetailView, FormView, CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import Http404
from django.template.defaultfilters import slugify

from glynt.apps.utils import AjaxableResponseMixin

from services import EnsureFounderService
from forms import StartupProfileSetupForm
from models import Founder

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
            
            'already_incorporated': startup.data.get('already_incorporated', False),
            'already_raised_capital': startup.data.get('already_raised_capital', False),
            'process_raising_capital': startup.data.get('process_raising_capital', False),

            'incubator_or_accelerator_name': startup.data.get('incubator_or_accelerator_name'),

            'agree_tandc': self.founder.data.get('agree_tandc', False),
        }})
        return form_class(**kwargs)

    def form_valid(self, form):
        form.save()
        return super(StartupProfileSetupView, self).form_valid(form=form)


class FounderProfileView(DetailView):
    model = Founder

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
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class CreateFounderView(AjaxableResponseMixin, CreateView):
    model = Founder
    http_method_names = [u'post']

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST
            first_name = data.__getitem__('founders-first_name')
            last_name = data.__getitem__('founders-last_name')
            user_name = "%s-%s" % (first_name, last_name)
            user_email = data.__getitem__('founders-email')
            user, is_new = User.objects.get_or_create(email=user_email, defaults={'username': user_name, 'first_name': first_name, 'last_name': last_name})
            founder = EnsureFounderService(user=user)
            founder.process()

            # Save form to new founder data

            return self.render_to_json_response({'message': "Founder saved", 'status': 200})
