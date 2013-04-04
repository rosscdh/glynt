# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User


import logging
logger = logging.getLogger('lawpal.service')


class InviteToJoinService(object):
    """ Invite an Email address to join"""
    inviting_user = None
    invitee_obje = () # [(email,name),]

    def __init__(self, inviting_user, invitee_obj, **kwargs):
        self.inviting_user = inviting_user
        logger.info('Invite request from User %d' % inviting_user.pk)
        self.invitee_obj = invitee_obj

        self.from_email, self.from_name = inviting_user.email, inviting_user.get_full_name()
        self.to_email, self.to_name = invitee_obj
        logger.info('Invite request from User (%s) %s -> %s to ' % (inviting_user.pk, self.from_email, self.to_email,))

        # get email template
        self.email_template = kwargs.get('email_template', 'lawyer')

        self.context = {
            'from': self.from_name
            ,'to': self.to_name
        }

    def process(self):
        logger.info('Sending Invite Email')
        send_templated_mail(
                template_name = self.email_template,
                template_prefix="invite/email/",
                from_email = admin_email,
                recipient_list = [self.to_email],
                context = self.context
        )