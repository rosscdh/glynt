# -*- coding: UTF-8 -*-
"""
Mixins that relate to the ToDo app
"""
from django.views.generic import View


class ProjectOppositeUserMixin(object):
    """
    Mixin to provide access to the view "object"'s project opposite_user
    """

    @property
    def opposite_user(self):
        try:
            return self.object.project.get_primary_lawyer().user if self.request.user.profile.is_customer else self.object.project.customer.user
        except AttributeError:
            return None


class CrocdocAttachmentSessionContextMixin(View):
    """
    Mixin to provide crocdoc session viewability
    """
    def get_context_data(self, **kwargs):
        context = super(CrocdocAttachmentSessionContextMixin, self).get_context_data(**kwargs)
        service = CrocdocAttachmentService(attachment=self.object)

        context.update({
            'session_key': service.session_key(user=self.request.user),
            'uuid': service.uuid,
            'view_url': service.view_url(user=self.request.user),
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