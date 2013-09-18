# -*- coding: UTF-8 -*-
from . import BaseEmailService


class NewActionEmailService(BaseEmailService):
    """
    Email Service
    Inform the relevant parties of a new action
    """
    verb = None
    whitelist_actions = [
        'todo.attachment.created',
        'todo.comment.created',
        'feedbackrequest.created.open',
        'feedbackrequest.created.closed',
        'project.lawyer_assigned',
    ]

    def __init__(self, **kwargs):
        self.verb = kwargs.get('verb', self.verb)

        super(NewActionEmailService, self).__init__(**kwargs)

    @property
    def can_send(self):
        return self.verb in self.whitelist_actions

    @property
    def email_template(self):
        return self.verb

    def send(self, **kwargs):
        if self.can_send:
            super(NewActionEmailService, self).send(**kwargs)
