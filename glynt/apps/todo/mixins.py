# -*- coding: UTF-8 -*-
"""
Mixins that relate to the ToDo app
"""
from django.views.generic import View

from .services import CrocdocAttachmentService

import logging
logger = logging.getLogger('django.request')


class ProjectOppositeUserMixin(object):
    """
    Mixin to provide access to the view "object"'s project opposite_user
    """

    @property
    def opposite_user(self):

        project = self.object if hasattr(self, 'object') and self.object.__class__.__name__ == 'Project' else None

        if project is None:
            project = self.project if hasattr(self, 'project') else None

        try:
            return project.get_primary_lawyer().user if self.request.user.profile.is_customer else project.customer.user
        except AttributeError:
            return None


class CrocdocAttachmentSessionContextMixin(View):
    """
    Mixin to provide crocdoc session viewability
    """
    crocdoc_service = None
    def __init__(self, *args, **kwargs):
        self.crocdoc_service = None
        super(CrocdocAttachmentSessionContextMixin, self).__init__(*args, **kwargs)

    def crocdoc(self):
        if self.crocdoc_service is None:
            self.crocdoc_service = CrocdocAttachmentService(attachment=self.object)
        return self.crocdoc_service

    @property
    def crocdoc_url(self):
        url = self.crocdoc().view_url(user=self.request.user)
        if url is None:
            logger.error('Could not get crocdoc url user: %s' % self.request.user)
        return url

    def get_context_data(self, **kwargs):
        context = super(CrocdocAttachmentSessionContextMixin, self).get_context_data(**kwargs)

        context.update({
            'session_key': self.crocdoc().session_key(user=self.request.user),
            'view_url': self.crocdoc_url,
            'uuid': self.crocdoc_service.uuid,
        })
        return context


class NumAttachmentsMixin(object):
    """
    A mixin specifically and only for ToDo ORM objects
    That allows us to store in the .data JSON object the number of attachments
    associated with this ToDo Object
    """
    @property
    def num_attachments(self):
        num = self.data.get('num_attachments', None)
        if num is None:
            num = self.attachments.count()
            self.data['num_attachments'] = num
            if self.pk is not None:
                self.save(update_fields=['data'])
        return num

    @num_attachments.setter
    def num_attachments(self, num):
        if self.pk and type(num) is int:
            self.data['num_attachments'] = num
            if self.pk is not None:
                self.save(update_fields=['data'])
            return num
        else:
            return 0

    def num_attachments_plus(self):
        num_attachments = self.data.get('num_attachments', 0)
        num_attachments += 1
        self.num_attachments = num_attachments

    def num_attachments_minus(self):
        num_attachments = self.data.get('num_attachments', 0)
        if num_attachments > 0:
            num_attachments -= 1
            self.num_attachments = num_attachments


class ToDoActivityMixin(object):
    """
    A Mixin to collect the todo and its related items "action" objects
    1. todo items (and by association their attachments, 
       attachments comments is setup to comment on the todo item and not the attachment itself)
    """
    def activity_stream(self, **kwargs):
        from actstream.models import Action
        return Action.objects.prefetch_related('actor').filter(target_object_id=self.pk,
                                     target_content_type=self.content_type(), **kwargs)

