# -*- coding: utf-8 -*-
from jsonview.decorators import json_view

from forms import InviteEmailForm
from tasks import send_invite_email

import logging
logger = logging.getLogger('django.request')

@json_view
def InviteEmailView(request):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        if request.method is 'POST':
            assert False
            #send_invite_email(from_user=request.user, (email,name,))
        return {
        
        }