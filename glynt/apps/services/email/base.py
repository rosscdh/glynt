# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.conf import settings
from django import template

from templated_email import send_templated_mail

from glynt.apps.services.abridge import SendEmailAsAbridgeEventMixin

import itertools
from bunch import Bunch

import logging
logger = logging.getLogger('lawpal.services')

admin_name, admin_email = settings.ADMINS[0]


class BaseEmailService(SendEmailAsAbridgeEventMixin):
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

    whitelist_actions = ['*']

    def __init__(self, *args, **kwargs):

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

        super(BaseEmailService, self).__init__(*args, **kwargs)

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

    @property
    def can_send(self):
        return '*' in self.whitelist_actions or self.verb in self.whitelist_actions

    def send(self, **kwargs):
        if self.can_send:

            logger.debug('Can Send Email {verb}'.format(verb=self.verb))

            self._subject = kwargs.get('subject', self._subject)
            self._message = kwargs.get('message', self._message)
            logger.debug('Preparing to send email: {subject} to {recipients}'.format(subject=self._subject, recipients=self.recipients))

            # merge kwargs into context
            self.context.update(kwargs)

            # in case of Abridge service exception
            if self.abridge_send(context=self.context, recipients=self.recipients) is False:

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

                    # ensure that the user is notified via the standard email method
                    email = Bunch(template_name=self.email_template,
                                  template_prefix=self.base_email_template_location,
                                  from_email='{from_name} via LawPal <{from_email}>'.format(from_name=self.from_name, from_email=self.from_email),
                                  recipient_list=[to_email],
                                  bcc=['founders@lawpal.com'] if settings.DEBUG is False else [],  # only bcc us in on live mails
                                  context=self.context)

                    send_templated_mail(**email)
