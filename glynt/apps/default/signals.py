# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.contrib.auth.signals import user_logged_in

import logging
logger = logging.getLogger('django.request')


@receiver(user_logged_in, dispatch_uid='user.on_user_logged_in')
def on_user_logged_in(sender, **kwargs):
    username = kwargs['user'].username
    logger.info('User: {user} has logged in'.format(user=username))

    next = kwargs['request'].session.get('next', None)

    if next is not None:
        logger.info('User {user} has a redirect {next}'.format(user=username, next=next))

        del kwargs['request'].session['next']  # delete the key

        return HttpResponseRedirect(next)