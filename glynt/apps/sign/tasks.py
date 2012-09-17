# -*- coding: utf-8 -*-
# tasks to handle the sending of signature invitations
from django.conf import settings
from django.core.urlresolvers import reverse

from templated_email import send_templated_mail
from celery import task

@task()
def send_signature_invite_email(**kwargs):
  """
  """
  # get document info
  # get email
  # process email
  document = kwargs['document']
  key_hash = kwargs['key_hash']
  from_name, from_email = settings.ADMINS[0]
  to_name, to_email = (kwargs['to_name'], kwargs['to_email'],)
  kwargs['from_name'] = from_name
  kwargs['from_email'] = from_email
  kwargs['document_name'] = document.name

  kwargs['sign_url'] = reverse('sign:default', kwargs={'hash': key_hash, 'pk': document.pk})

  send_templated_mail(
          template_name = 'invite_to_sign',
          template_prefix="sign/email/",
          from_email = from_email,
          recipient_list = [to_email],
          context = kwargs
  )
  pass