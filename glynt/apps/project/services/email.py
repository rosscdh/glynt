# -*- coding: utf-8 -*-
from django.conf import settings

from django.contrib.sites.models import Site

from glynt.apps.project import PROJECT_STATUS

from templated_email import send_templated_mail
from bunch import Bunch

import logging
logger = logging.getLogger('lawpal.services')

site_email = settings.DEFAULT_FROM_EMAIL


class SendProjectEmailsService(object):
    """ Class to send email to appropriate persons involved in and project.
    is applied when creating an project; as well as commenting on an project
    """
    mail_template_name = 'project_notice_email'

    def __init__(self, project, sender, recipients, notification=None, **kwargs):
        self.project = project
        self.is_new_project = kwargs.get('is_new_project', False)
        self.sender = sender
        self.sender_is_lawyer = sender.profile.is_lawyer
        self.recipients = recipients
        self.notification = notification
        self.site = Site.objects.get_current()

        kwargs.update({
            'is_new': self.is_new_project,
            'project_status': PROJECT_STATUS.get_desc_by_value(project.status),
            'sender_is_lawyer': self.sender_is_lawyer,
            'from_name': self.sender.get_full_name(),
            'from_email': self.sender.email,
            'from': self.sender,
            'project': self.project,
            'notification': self.notification,
            'message': self.message,
            'comment': self.notification.description if self.notification else None,
            'project_statement': self.project.project_statement,
            'site': self.site,
        })

        self.context = kwargs

    @property
    def message(self):
        notice = self.notification

        ctx = {
            'actor': notice.actor.get_full_name(),
            'verb': notice.verb,
            'action_object': notice.action_object,
            'target': self.project.customer if self.sender_is_lawyer else self.project.lawyer,
            'timesince': notice.timesince()
        }
        return u'%(actor)s commented on the Project with %(target)s' % ctx

    @property
    def recipient_list(self):
        if type(self.recipients) in [list, tuple]:
            recipients = self.recipients
        else:
            recipients = [Bunch(name=u[0], email=u[1]) for u in settings.NOTICEGROUP_EMAIL]
        return [u.email for u in recipients]

    def process(self):
        send_templated_mail(
              template_name = self.mail_template_name,
              template_prefix="email/",
              from_email = site_email,
              recipient_list = self.recipient_list,
              context = self.context
        )


class SendNewProjectEmailsService(SendProjectEmailsService):
    mail_template_name = 'project_created'

    def __init__(self, project, sender, **kwargs):
        super(SendNewProjectEmailsService, self).__init__(project=project, sender=sender, recipients=None, notification=None)
        self.context.update({
            'customer': self.project.customer,
            'company': self.project.customer.primary_company,
        })

    @property
    def message(self):
        ctx = {
            'actor': self.sender,
            'project': self.project,
            'id': self.project.pk,
        }

        return u'%(actor)s created a new Project (%(project)s):%(id)d which needs to be matched with a lawyer' % ctx
