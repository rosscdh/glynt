# -*- coding: UTF-8 -*-
from . import BaseEmailService


class NewActionEmailService(BaseEmailService):
    """
    Email Service
    Inform the relevant parties of a new action
    """
    email_template = 'new.action'


# class TodoCommentEmailService(BaseEmailService):
#     """
#     Email Service
#     Inform the relevant parties of a new comment
#     """
#     email_template = 'new.action'

#     @property
#     def message(self):
#         return '{from_name} commented on a checklist item.\n\n' \
#                '{comment}\n'.format(from_name=self.from_name, comment=self.context.get('comment').comment)