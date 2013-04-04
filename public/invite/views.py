# -*- coding: utf-8 -*-
from jsonview.decorators import json_view

from forms import InviteEmailForm

import logging
logger = logging.getLogger('django.request')

#@json_view
def InviteEmailView(request):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        if request.method == 'POST':
            invitees_list = zip(request.POST.getlist('email'), request.POST.getlist('name'))
            invite_type = request.POST.get('invite_type', 'lawyer')

            for email,name in invitees_list:

                form = InviteEmailForm({'email': email, 'name': name, 'invite_type':invite_type})

                if form.is_valid():
                    form.save(user=request.user)

            assert False
        return {
        
        }