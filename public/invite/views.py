# -*- coding: utf-8 -*-
from jsonview.decorators import json_view
from django.utils import simplejson as json
from forms import InviteEmailForm

import logging
logger = logging.getLogger('django.request')

@json_view
def InviteEmailView(request):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        errors = success = []
        c = 0
        if request.method == 'POST':
            invitees_list = zip(request.POST.getlist('email'), request.POST.getlist('name'))
            invite_type = request.POST.get('invite_type', 'lawyer')

            for email,name in invitees_list:
                form = InviteEmailForm({'email': email, 'name': name, 'invite_type':invite_type})

                if form.is_valid():
                    form.save(user=request.user)
                    success.append('%s: %s' % (name,email,))
                else:
                    er = ','.join(['%d %s: %s' % (c, k, ', '.join(v),) for k, v in form.errors.items()])
                    errors.append(er)
                c = c+1

        success = ' '.join(success)
        return {
            'message': 'Invited %s' % success,
            'errors': json.dumps(errors)
        }