# -*- coding: utf-8 -*-
""" tasks for the Firm objects """
from django.conf import settings
from django.core.urlresolvers import reverse

from templated_email import send_templated_mail

from celery.task import task

import logging
logger = logging.getLogger('django.request')


@task()
def new_firm_email_task(**kwargs):
  """
  """
  firm = kwargs.get('firm', 'No Firm is present')
  logger.info('Sending new_firm_email_task: %s' % firm)
  send_templated_mail(
          template_name = 'firm_created',
          template_prefix="email/info/",
          from_email = settings.ADMINS[0][1],
          recipient_list = [email for name,email in settings.NOTICEGROUP_EMAIL],
          context = kwargs
  )
