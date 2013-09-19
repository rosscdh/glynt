# -*- coding: UTF-8 -*-
from . import BaseEmailService


class NewActionEmailService(BaseEmailService):
    """
    Email Service
    Inform the relevant parties of a new action
    """
    actor=None
    object=None
    project=None
    verb=None
    whitelist_actions=[
        'todo.attachment.created',
        'todo.comment.created',
        'feedbackrequest.opened',
        'feedbackrequest.closed',
        'project.lawyer_assigned',
    ]

    def __init__(self, **kwargs):
        self.actor = kwargs.get('actor', self.actor)
        self.object = kwargs.get('object', self.object)
        self.project = kwargs.get('project', self.project)
        self.verb = kwargs.get('verb', self.verb)

        super(NewActionEmailService, self).__init__(**kwargs)

        self.context.update({
            'actor': self.actor,
            'object': self.object,
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
            super(NewActionEmailService, self).send(**kwargs)
