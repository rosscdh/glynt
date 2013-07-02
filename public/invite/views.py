# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from forms import InviteEmailForm

import logging
logger = logging.getLogger('django.request')


def InviteEmailView(request):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        message = []
        c = 0
        if request.method == 'POST':
            invitees_list = zip(request.POST.getlist('email'), request.POST.getlist('name'))
            invite_type = request.POST.get('invite_type', 'lawyer')

            for email,name in invitees_list:
                form = InviteEmailForm({'email': email, 'name': name, 'invite_type':invite_type})

                if form.is_valid():
                    form.save(user=request.user)
                    er = None
                else:
                    er = ','.join(['%s: %s' % (k, ', '.join(v),) for k, v in form.errors.items()])

                message.append({'name': name, 'email': email, 'errors':er} )
                c = c+1

        return HttpResponse(json.dumps(message), mimetype="application/json")