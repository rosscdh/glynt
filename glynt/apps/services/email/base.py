# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.conf import settings
from django import template


from templated_email import send_templated_mail

admin_name, admin_email = settings.ADMINS[0]

from bunch import Bunch

import itertools

import logging
logger = logging.getLogger('lawpal.services')


class BaseEmailService(object):
    """
    Base Email Service
    Provides template and basic sending properties
    """
    email_template = None
    base_email_template_location = 'email/'

    _subject = None
    _message = None

    from_name = None

    to_name = None
    from_email = None
    to_email = None

    def __init__(self, **kwargs):
        self._subject = kwargs.get('subject', self._subject)
        self._message = kwargs.get('message', self._message)
        self.from_name = kwargs.get('from_name', admin_name)
        self.from_email = kwargs.get('from_email', admin_email)

        self.to_name = kwargs.get('to_name')
        # Allow multiple recipients or a single to_email giving preference to recipients
        self.to_email = kwargs.get('to_email')
        self.recipients = kwargs.get('recipients', [])

        # set email template context
        self.context = kwargs

        assert self.subject
        assert self.email_template
        assert self.from_name
        assert self.from_email

        if self.recipients:
            """ extract list of recipients name, email from the passed in recipients """
            assert type(self.recipients) in [list, tuple, itertools.chain]

            recipients = []

            for u in self.recipients:
                if type(u) in [User]:
                    """ dont add email to recipient if its the same as the from_email """
                    if u.email != self.from_email:
                        recipients.append((u.get_full_name(), u.email,))
            self.recipients = recipients

        else:
            assert self.to_name
            assert self.to_email
            self.recipients = ((self.to_name, self.to_email),)

        self.context.update({
            'subject': self.subject,
            'message': self.message,
            'from_name': self.from_name,
            'from_email': self.from_email,
            'STATIC_URL': settings.STATIC_URL,
        })

        logger.info('Initialized BaseEmailService with context: {context}'.format(context=self.context))

    def _templatize_context(self, target, **kwargs):
        t = template.Template(target)
        c = template.Context(kwargs)
        return t.render(c)

    @property
    def subject(self):
        return self._templatize_context(target=self._subject, **self.context)

    @property
    def message(self):
        return self._templatize_context(target=self._message, **self.context)

    def process(self, **kwargs):
        return self.send(**kwargs)

    def send(self, **kwargs):
        self._subject = kwargs.get('subject', self._subject)
        self._message = kwargs.get('message', self._message)
        logger.debug('Preparing to send email: {subject} to {recipients}'.format(subject=self._subject, recipients=self.recipients))

        # merge kwargs into context
        self.context.update(kwargs)

        # Loop over the recipients list
        for to_name, to_email in self.recipients:

            self.context.update({
                'to_name': to_name,
                'to_email': to_email,
            })
            # Update subject
            self.context.update({
                'subject': self.subject,
                'message': self.message,
            })

            logger.info('Sending Email to: {to} email_template: {email_template} with context: {context}'.format(to=self.to_email, email_template=self.email_template, context=self.context))

            email = Bunch(template_name=self.email_template,
                          template_prefix=self.base_email_template_location,
                          from_email='{from_name} via LawPal <{from_email}>'.format(from_name=self.from_name, from_email=self.from_email),
                          recipient_list=[to_email],
                          bcc=['founders@lawpal.com'],
                          context=self.context)

            if settings.DEBUG == True:
                email.pop('bcc')

            send_templated_mail(**email)
