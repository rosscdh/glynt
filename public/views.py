from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

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
