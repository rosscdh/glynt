# -*- coding: utf-8 -*-
"""
Set of View Mixins that will allow us to implement django-rulez
https://github.com/chrisglass/django-rulez
"""
from django.core.exceptions import PermissionDenied

import logging
logger = logging.getLogger('django.request')


class RulezMixin(object):
    """
    Mixin that allows us to call the model methods
    can_edit
    can_read
    can_delete
    defined by django-rulez *see its docs
    """
    def can_read(self, obj, user=None):
        if user is None and hasattr(self, 'request'):
            user = self.request.user

        if user is not None:
            if hasattr(obj, 'can_read'):
                if not obj.can_read(user):
                    raise PermissionDenied()
            else:
                logger.critical('{obj} needs to have django-rulez:can_read method defined'.format(obj=obj))


    def can_edit(self, obj, user=None):
        if user is None and hasattr(self, 'request'):
            user = self.request.user

        if user is not None:
            if hasattr(obj, 'can_edit'):
                if not obj.can_edit(user):
                    raise PermissionDenied()
            else:
                logger.critical('{obj} needs to have django-rulez:can_read method defined'.format(obj=obj))
