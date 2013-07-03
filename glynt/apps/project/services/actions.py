# -*- coding: utf-8 -*-
from django.conf import settings

from glynt.apps.project import PROJECT_STATUS

from notifications import notify
import user_streams
import datetime

import logging
logger = logging.getLogger('lawpal.services')

site_email = settings.DEFAULT_FROM_EMAIL


class BaseProjectService(object):
    """ The base class to handle opening and closing and re-opening Project objects """
    target_status = PROJECT_STATUS.open
    verb = 'opened'
    actioning_user = None
    recipient = None

    def __init__(self, project, actioning_user, **kwargs):
        self.project = project
        self.actioning_user = actioning_user

    def process(self):
        """ set the project project_status
        and return the notification description so that it can be rendered
        in json response """
        self.project.project_status = self.target_status
        self.project.save(update_fields=['project_status'])
        return self.notifications()

    @property
    def recipient(self):
        return self.project.customer.user if self.actioning_user.profile.is_lawyer else self.project.lawyer.user

    def notifications(self):
        # send notification
        description = '%s (%s) %s the Project' % (self.actioning_user.profile.non_specific_title, \
                                                    self.actioning_user, self.verb)

        notify.send(self.actioning_user, recipient=self.recipient, verb=self.verb, action_object=self.project,
                    description=description, target=self.project, project_pk=self.project.pk, \
                    closed_by=self.actioning_user.pk, directed_at=self.recipient.pk, \
                    lawyer_pk=self.project.lawyer.user.pk, customer_pk=self.project.customer.user.pk, \
                    date_closed=datetime.datetime.utcnow())

        # Log activity to stream
        user_streams.add_stream_item(self.recipient, description, self.project)
        user_streams.add_stream_item(self.actioning_user, description, self.project)

        return description


class OpenProjectService(BaseProjectService):
    """ Service to assist in opening a class """
    target_status = PROJECT_STATUS.open
    verb = 'opened'


class CloseProjectService(BaseProjectService):
    """ Service to assist in closing a class """
    target_status = PROJECT_STATUS.closed
    verb = 'closed'


class ReOpenProjectService(BaseProjectService):
    """ Service to assist in re-opening a class """
    target_status = PROJECT_STATUS.open
    verb = 're-opened'