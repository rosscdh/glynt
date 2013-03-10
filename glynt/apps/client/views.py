from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.core.urlresolvers import reverse

from socialregistration.contrib.facebook_js.models import FacebookProfile
from userena import signals as userena_signals

from glynt.apps.document.models import DocumentTemplate, ClientCreatedDocument
from forms import SignupForm, AuthenticationForm

import logging
logger = logging.getLogger('django.request')


class SignupView(FormView):
    template_name = 'userena/signup_form.html'
    form_class = SignupForm

    def get_success_url(self):
        return reverse('client:dashboard')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            messages.info(request, _('Welcome, you have successfully signed up. Please remember to check your email and activate your account once you recieve our welcome email.'))
            user = form.save()
            logger.info('A user has signed up %s' % user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LoginView(FormView):
    """ Primative login """
    template_name = 'client/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse('client:dashboard')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        user = authenticate(username=request.POST.get('username',None), password=request.POST.get('password',None))

        if user is None:
            logger.warn('Incorrect login attempt user: %s' % request.POST.get('username',None))
        else:
            if user.is_active:
                login(request, user)
                if request.GET.get('next') is not None:
                    self.success_url = request.GET.get('next')
                messages.success(request, _('Welcome, you have successfully logged in.'))

                logger.info('LoggedIn user: %s' % user)

                return self.form_valid(form)
            else:
                messages.info(request, _('Sorry, but your Account has yet to be acivated.'))
                logger.info('Inactive login attempt user: %s' % request.POST.get('username',None))

        return self.form_invalid(form)


class DashboardView(TemplateView):
    template_name = 'client/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['public_document_list'] = DocumentTemplate.public_objects.select_related('doc_category').all()
        context['my_document_list'] = ClientCreatedDocument.active_objects.filter(owner=self.request.user)

        context['csrf_raw_token'] = get_token(self.request)

        return context
