# -*- coding: utf-8 -*-
""" Tasks related to Lawyer accounts and profiles """
from django.conf import settings

from celery.task import task

from templated_email import send_templated_mail
from glynt.apps.default.templatetags.glynt_helpers import current_site_domain
from django.core.urlresolvers import reverse

import logging
logger = logging.getLogger('lawpal.services')


SITE_EMAIL = settings.DEFAULT_FROM_EMAIL


@task()
def send_profile_setup_email(**kwargs):
    to_user = kwargs.get('user', None)

    if to_user is None:
        logger.error('No user was passed into tasks.send_profile_setup_email')
    else:
        to_user_name = to_user.get_full_name() if to_user.get_full_name() != '' else to_user.username

        to_name, to_email = (to_user_name, to_user.email)

        kwargs.update({
            'to_name': to_name, 
            'to_email': to_email,
            'profile_url': '%s%s' % (current_site_domain(), reverse('lawyer:profile', kwargs={'slug': to_user.username})),
        })

        logger.info('Sending Profile Setup Confirm email: %s' % kwargs.get('profile_url'))

        send_templated_mail(
            template_name = 'lawyer/profile_setup_confirm',
            template_prefix = "email/",
            from_email = SITE_EMAIL,
            recipient_list = [to_email],
            bcc = [e for n,e in settings.MANAGERS],
            context = kwargs
        )
