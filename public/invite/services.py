# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from templated_email import send_templated_mail

admin_name, admin_email = settings.ADMINS[0]

import logging
logger = logging.getLogger('lawpal.services')


class InviteToJoinService(object):
    """ Invite an Email address to join"""
    inviting_user = None
    invitee_obje = () # [(email,name),]

    def __init__(self, inviting_user, invitee_obj, **kwargs):
        self.inviting_user = inviting_user
        logger.info('Invite request from User %d' % inviting_user.pk)
        self.invitee_obj = invitee_obj

        user_full_name = inviting_user.get_full_name() or inviting_user.username

        self.from_email, self.from_name = inviting_user.email, user_full_name
        self.to_email, self.to_name = invitee_obj

        logger.info('Invite request from User (%s) %s -> %s to ' % (inviting_user.pk, self.from_email, self.to_email,))

        # get email template
        self.email_template = kwargs.get('email_template', 'lawyer')
        self.context = kwargs

        assert self.from_name
        assert self.to_name
        assert self.from_email
        assert self.to_email

        self.context.update({
            'from_name': self.from_name
            ,'to_name': self.to_name
            ,'from_email': self.from_email
            ,'to_email': self.to_email
        })

    def process(self):
        logger.info('Sending Invite Email')

        send_templated_mail(
                template_name = self.email_template,
                template_prefix = "invite/email/",
                from_email = '{from_name} via LawPal <{admin_email}>'.format(from_name=self.from_name, admin_email=admin_email),
                recipient_list = [self.to_email],
                bcc = ['founders@lawpal.com'],
                context = self.context,
        )
