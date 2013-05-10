# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from public.forms import ContactForm
from public.tasks import send_contactus_email



import logging
logger = logging.getLogger('django.request')


class PublicHomepageView(TemplateView):
    template_name='public/homepage.html'

    def get_template_names(self):
        if self.request.user.is_authenticated():
            return ['lawyer/welcome.html']
        else:
            return [self.template_name]


class LoggedInRedirectView(RedirectView):
    """ View to handle generic logged in from Oauth Providers """
    def get_redirect_url(self):
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
        logger.info('Contact us from: %s (%s) message: %s' % (form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'],) )

        # try:
        #     send_contactus_email.delay(from_name=form.cleaned_data['name'], from_email=form.cleaned_data['email'], message=form.cleaned_data['message'])
        # except:
        send_contactus_email(from_name=form.cleaned_data['name'], from_email=form.cleaned_data['email'], message=form.cleaned_data['message'])

        messages.success(self.request, "Message sent, thanks!")

        return super(ContactUsView, self).form_valid(form)

