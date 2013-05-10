# -*- coding: utf-8 -*-
# tasks to handle the sending of invitations
from django.conf import settings
from django.core.mail import send_mail
from celery.task import task

import logging
logger = logging.getLogger('django.request')

RECIPIENTS = [email for name,email in settings.MANAGERS]


@task()
def send_contactus_email(from_name, from_email, message, **kwargs):
    """ from user = request.user 
    to_object = (email,name)
    """
    logger.info('Sending contact us from: %s (%s) message: %s' % (from_name, from_email, message,) )

    send_mail('%s has contacted LawPal' % from_name, message, from_email, RECIPIENTS, fail_silently=False)