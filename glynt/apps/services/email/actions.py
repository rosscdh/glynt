# -*- coding: UTF-8 -*-
from . import BaseEmailService

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
        'todo.attachment.created',
        'todo.comment.created',
        'feedbackrequest.opened',
        'feedbackrequest.closed',
        'project.lawyer_assigned',
    ]

    def __init__(self, **kwargs):
        self.actor = kwargs.pop('actor', None)

        self.target = kwargs.pop('target', None)
        self.project = kwargs.pop('project', None)
        self.verb = kwargs.pop('verb', None)
        
        super(NewActionEmailService, self).__init__(**kwargs)

        self.context.update({
            'actor': self.actor,
            'object': self.target,
            'project': self.project,
        })

    @property
    def can_send(self):
        return self.verb in self.whitelist_actions

    @property
    def email_template(self):
        return 'actions/{template}'.format(template=self.verb)

    def send(self, **kwargs):
        if self.can_send:
            logger.debug('Can Send Email {verb}'.format(verb=self.verb))

            super(NewActionEmailService, self).send(**kwargs)
