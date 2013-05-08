from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from public.forms import ContactForm
from django.views.generic.edit import FormView

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
    success_url = '/thanks/'

    def get_template_names(self):
        if self.request.is_ajax():
            return ['public/contact_us_modal.html']
        else:
            return [self.template_name]

    def form_valid(self, form):
        #if self.request.user.is_authenticated():
        send_mail('%s has contacted LawPal' % form.cleaned_data['name'], form.cleaned_data['message'], form.cleaned_data['email'], ['rob@lawpal.com'], fail_silently=False)

        return super(ContactUsView, self).form_valid(form)


class ThankYouView(TemplateView):
    template_name = 'public/thanks.html'

    def get_template_names(self):
        if self.request.is_ajax():
            return ['public/thanks_modal.html']
        else:
            return [self.template_name]