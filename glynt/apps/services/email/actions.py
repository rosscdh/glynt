# -*- coding: UTF-8 -*-
from . import BaseEmailService


class NewActionEmailService(BaseEmailService):
    """
    Email Service
    Inform the relevant parties of a new action
    """
    email_template = 'new.action'
