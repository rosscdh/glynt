# -*- coding: UTF-8 -*-
from .base import BaseEmailService

import logging
logger = logging.getLogger('lawpal.services')


class NewActionEmailService(BaseEmailService):
    """
    Email Service
    Inform the relevant parties of a new action
    """
    actor = None
    target = None
    project = None
    verb = None
    whitelist_actions = [
        'project.comment.created',
        'project.lawyer_engage.comment.created',
        'project.lawyer_assigned',
        'todo.attachment.created',
        'todo.comment.created',
        'feedbackrequest.opened',
        'feedbackrequest.closed',
    ]

    def __init__(self, **kwargs):
        self.actor = kwargs.pop('actor', None)

        self.target = kwargs.pop('target', None)
        self.project = kwargs.pop('project', None)
        self.verb = kwargs.pop('verb', None)

        # pass in content group so that abridge service can be used
        kwargs['content_group'] = self.project.__unicode__() if self.project is not None else None


        super(NewActionEmailService, self).__init__(**kwargs)

        self.context.update({
            'actor': self.actor,
            'object': self.target,
            'project': self.project,
        })

    @property
    def email_template(self):
        return 'actions/{template}'.format(template=self.verb)