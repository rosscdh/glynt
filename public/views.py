# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import Http404
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from public.forms import ContactForm
from public.tasks import send_contactus_email
from glynt.apps.customer import CustomerLoginLogic

import logging
logger = logging.getLogger('django.request')


class PublicHomepageView(TemplateView):
    template_name = 'public/homepage.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.profile.is_customer:
                return CustomerLoginLogic(user=request.user).redirect()

        return super(PublicHomepageView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        # get from session
        user_class_name = self.request.session.get('user_class_name', 'lawyer')

        template_name = self.template_name
        if self.request.user.is_authenticated():
            # we are logged in.. redirect based on the user_class_name
            if user_class_name == 'lawyer':
                template_name = 'lawyer/welcome.html'

            if user_class_name == 'customer':
                template_name = 'customer/welcome.html'

        return [template_name]


class UserClassSessionRedirectView(RedirectView):
    """ View to set a session that helps us determine what class a user is logging in as,
    based on the session value
    """
    permanent = False  # status = 302 not 301 (permanent)

    def get_redirect_url(self, **kwargs):
        """ if the user has already signed up and has set a password then continue normally
        otherwise show them the form """

        user_class_name = kwargs.get('user_class_name', 'customer')  # default to customer
        login_type = kwargs.get('login_type', 'linkedin')  # default to linkedin

        self.request.session['user_class_name'] = user_class_name

        logging.debug('logging in as user_class_name: %s using %s' % (user_class_name, login_type))

        if user_class_name:
            url = reverse('socialauth_begin', args=[login_type])
        else:
            raise Http404("User Class %s is not Defined" % user_class_name)

        logging.debug('redirecting user_class_name: %s to : %s' % (user_class_name, url,))
        return url


class UserClassLoggedInRedirectView(RedirectView):
    """ View to handle generic logged in from Oauth Providers """
    def get_redirect_url(self, **kwargs):
        """ if the user has already signed up and has set a password then continue normally
        otherwise show them the form """
        if self.request.user.password == '!':
            url = reverse('client:confirm_signup', kwargs={'slug': self.request.user.username})
        else:
            url = reverse('public:homepage')

        return url


class ContactUsView(FormView):
    template_name = 'public/contact-us.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('public:contact_us')

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'request': self.request}) # add the request to the form
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(ContactUsView, self).get_context_data(**kwargs)
        kwargs.update({
            'template_to_extend': 'base-slim.html' if self.request.is_ajax() else 'base.html'
        })
        return kwargs

    def form_valid(self, form):
        logger.info('Contact us from: %s (%s) message: %s' % (form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'],))

        send_contactus_email(from_name=form.cleaned_data['name'], from_email=form.cleaned_data['email'], message=form.cleaned_data['message'])

        messages.success(self.request, "Message sent, thanks!")

        return super(ContactUsView, self).form_valid(form)
