# -*- coding: utf-8 -*-
from django.conf import settings

from django.contrib.sites.models import Site

from notifications import notify

from glynt.apps.startup.services import EnsureFounderService, EnsureStartupService
from glynt.apps.engage import generate_engagement_slug
from glynt.apps.engage.models import Engagement
from glynt.apps.engage import ENGAGEMENT_STATUS

from templated_email import send_templated_mail
from bunch import Bunch

import logging
logger = logging.getLogger('lawpal.services')

site_email = settings.DEFAULT_FROM_EMAIL


class EngageLawyerAsStartupService(object):
    """ Allow a startup to engage a Lawyer """

    def __init__(self, user, lawyer, startup_name, **kwargs):
        self.user = user
        self.lawyer = lawyer
        self.startup_name = startup_name

        self.form = kwargs.pop('form', None)

        self.data = kwargs

    def process(self):
        founder_service = EnsureFounderService(user=self.user, **self.data)
        self.founder = founder_service.process()

        startup_service = EnsureStartupService(name=self.startup_name, founder=self.founder, **self.data)
        self.startup = startup_service.process()

        engagement, is_new = self.save_engagement()

        self.notify(self.engagement, is_new)

        return self.engagement

    def save_engagement(self):
        self.engagement, is_new = Engagement.objects.get_or_create(startup=self.startup, founder=self.founder, lawyer=self.lawyer)
        self.engagement.data = self.data
        self.engagement.save(update_fields=['data'])
        return self.engagement, is_new


    def notify(self, engagement, is_new):
        verb = engagement_action = 'engagement_updated'
        description = '%s Updated the Engagement Lead for %s' % (self.founder, self.lawyer,)

        if is_new:
            verb = engagement_action = 'engagement_created'
            description = '%s Created a new Lead for %s' % (self.founder, self.lawyer,)

        notify.send(self.founder.user, recipient=self.lawyer.user, verb=verb, action_object=self.engagement,
                    description=description , target=self.lawyer, engagement_action=engagement_action, engagement_pk=self.engagement.pk, lawyer_pk=self.lawyer.user.pk, founder_pk=self.founder.user.pk)



class SendEngagementEmailsService(object):
    """ Class to send email to appropriate persons involved in and engagement.
    is applied when creating an engagement; as well as commenting on an engagement
    """

    def __init__(self, engagement, sender, recipients, notification, **kwargs):
        self.engagement = engagement
        self.is_new_engagement = kwargs.get('is_new_engagement', False)
        self.sender = sender
        self.sender_is_lawyer = sender.profile.is_lawyer
        self.recipients = recipients
        self.notification = notification
        self.site = Site.objects.get_current()

        kwargs.update({
            'is_new': self.is_new_engagement,
            'engagement_status': ENGAGEMENT_STATUS.get_desc_by_value(engagement.engagement_status),
            'sender_is_lawyer': self.sender_is_lawyer,
            'from_name': self.sender.get_full_name(),
            'from_email': self.sender.email,
            'from': self.sender,
            'engagement': self.engagement,
            'notification': self.notification,
            'message': self.message,
            'comment': self.notification.description,
            'engagement_statement': self.engagement.engagement_statement,
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
            'target': self.engagement.founder if self.sender_is_lawyer else self.engagement.lawyer,
            'timesince': notice.timesince()
        }
        return u'%(actor)s commented on the Engagement with %(target)s' % ctx

    @property
    def recipient_list(self):
        if type(self.recipients) in [list,tuple]:
            recipients = self.recipients
        else:
            recipients = [Bunch(name=u[0], email=u[1]) for u in settings.NOTICEGROUP_EMAIL]
        return [u.email for u in self.recipients]

    def process(self):
        send_templated_mail(
              template_name = 'engagement_notice_email',
              template_prefix="email/",
              from_email = site_email,
              recipient_list = self.recipient_list,
              context = self.context
        )
