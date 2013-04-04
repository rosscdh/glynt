# -*- coding: utf-8 -*-
# tasks to handle the sending of invitations
from django.conf import settings

from templated_email import send_templated_mail

from celery.task import task

from services import InviteUserService

import logging
logger = logging.getLogger('django.request')


@task()
def send_invite_email(from_user, to_object, **kwargs):
    """ from user = request.user 
    to_object = (email,name)
    """
    invite_service = InviteUserService(inviting_user=from_user, invitee_obj=to_object)
    invite_service.process()