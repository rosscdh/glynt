from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse

import logging
logger = logging.getLogger('django.request')


class LoggedInRedirectView(RedirectView):
    """ View to handle generic logged in from Oauth Providers """
    def get_redirect_url(self):
        url = reverse('public:lawyer')
        return url
