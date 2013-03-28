# -*- coding: utf-8 -*-
# tasks to handle the sending of signature invitations
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from templated_email import send_templated_mail
from django_rq import job

import user_streams
import logging
logger = logging.getLogger('django.request')


@job
def send_signature_invite_email(**kwargs):
  """
  """
  # get document info
  # get email
  # process email
  document = kwargs['document']
  key_hash = kwargs['key_hash']
  admin_name, admin_email = settings.ADMINS[0]

  to_name, to_email = (kwargs.get('to_name', 'No Name'), kwargs.get('to_email', 'noone@lawpal.com'),)
  invited_by_pk, invited_by_name, invited_by_email = (kwargs.get('invited_by_pk', None), kwargs.get('invited_by_name','No Invited By'), kwargs.get('invited_by_email','noinvitedby@lawpal.com'),)

  kwargs['from_name'] = invited_by_name
  kwargs['from_email'] = invited_by_email
  kwargs['document_name'] = document.name

  kwargs['sign_url'] = reverse('sign:default', kwargs={'hash': key_hash, 'pk': document.pk})

  logger.debug('Sending invite email url: %s'%kwargs['sign_url'])

  send_templated_mail(
          template_name = 'invite_to_sign',
          template_prefix="sign/email/",
          from_email = admin_email,
          recipient_list = [to_email],
          context = kwargs
  )
  # Send notification
  user = User.objects.get(pk=invited_by_pk)
  user_streams.add_stream_item(user, _('You invited %s to sign "<a href="%s">%s</a>"' % (to_name, document.get_absolute_url(), document.name,)), document)


@job
def send_signature_acquired_email(**kwargs):
  """
  """
  # get document info
  # get email
  # process email
  document = kwargs['document']
  key_hash = kwargs['key_hash']
  admin_name, admin_email = settings.ADMINS[0]
  to_name, to_email = (kwargs['to_name'], kwargs['to_email'],)
  invited_by_pk, invited_by_name, invited_by_email = (kwargs['invited_by_pk'], kwargs['invited_by_name'], kwargs['invited_by_email'],)
  kwargs['from_name'] = invited_by_name
  kwargs['from_email'] = invited_by_email
  kwargs['document_name'] = document.name

  kwargs['review_signatures_url'] = reverse('sign:default', kwargs={'pk': document.pk, 'hash': key_hash})

  logger.debug('Sending acquired signature email url: %s'%kwargs['review_signatures_url'])

  send_templated_mail(
          template_name = 'signature_acquired',
          template_prefix="sign/email/",
          from_email = admin_email,
          recipient_list = [invited_by_email],
          context = kwargs
  )
  # Send notification
  user = User.objects.get(pk=invited_by_pk)
  user_streams.add_stream_item(user, _('%s has signed "<a href="%s">%s</a>"' % (to_name, document.get_absolute_url(), document.name,)), document)
