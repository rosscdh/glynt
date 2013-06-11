# -*- coding: utf-8 -*-
from django.conf import settings

from glynt.apps.engage import ENGAGEMENT_STATUS

from notifications import notify
import user_streams
import datetime

import logging
logger = logging.getLogger('lawpal.services')

site_email = settings.DEFAULT_FROM_EMAIL


class BaseEngagementService(object):
    """ The base class to handle opening and closing and re-opening Engagement objects """
    target_status = ENGAGEMENT_STATUS.open
    verb = 'opened'
    actioning_user = None
    recipient = None

    def __init__(self, engagement, actioning_user, **kwargs):
        self.engagement = engagement
        self.actioning_user = actioning_user

    def process(self):
        """ set the engagement engagement_status
        and return the notification description so that it can be rendered
        in json response """
        self.engagement.engagement_status = self.target_status
        self.engagement.save(update_fields=['engagement_status'])
        return self.notifications()

    @property
    def recipient(self):
        return self.engagement.founder.user if self.actioning_user.profile.is_lawyer else self.engagement.lawyer.user

    def notifications(self):
        # send notification
        description = '%s (%s) %s the Engagement' % (self.actioning_user.profile.non_specific_title, \
                                                    self.actioning_user, self.verb)

        notify.send(self.actioning_user, recipient=self.recipient, verb=self.verb, action_object=self.engagement,
                    description=description, target=self.engagement, engagement_pk=self.engagement.pk, \
                    closed_by=self.actioning_user.pk, directed_at=self.recipient.pk, \
                    lawyer_pk=self.engagement.lawyer.user.pk, founder_pk=self.engagement.founder.user.pk, \
                    date_closed=datetime.datetime.utcnow())

        # Log activity to stream
        user_streams.add_stream_item(self.recipient, description, self.engagement)
        user_streams.add_stream_item(self.actioning_user, description, self.engagement)

        return description


class OpenEngagementService(BaseEngagementService):
    """ Service to assist in opening a class """
    target_status = ENGAGEMENT_STATUS.open
    verb = 'opened'


class CloseEngagementService(BaseEngagementService):
    """ Service to assist in closing a class """
    target_status = ENGAGEMENT_STATUS.closed
    verb = 'closed'


class ReOpenEngagementService(BaseEngagementService):
    """ Service to assist in re-opening a class """
    target_status = ENGAGEMENT_STATUS.open
    verb = 're-opened'