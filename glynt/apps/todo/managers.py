# -*- coding: UTF-8 -*-
from django.db import models
from glynt.apps.todo import TODO_STATUS, FEEDBACK_STATUS


class DefaultToDoManager(models.Manager):
    """
    Manager for ToDos
    """
    def get_queryset(self):
            return super(DefaultToDoManager, self).get_queryset().filter(is_deleted=False)

    def deleted(self, **kwargs):
        return self.filter(is_deleted=True, **kwargs)

    def new(self, **kwargs):
        return self.filter(status=TODO_STATUS.new, is_deleted=False).filter(**kwargs)

    def open(self, **kwargs):
        return self.filter(status=TODO_STATUS.open, is_deleted=False).filter(**kwargs)

    def pending(self, **kwargs):
        return self.filter(status=TODO_STATUS.pending, is_deleted=False).filter(**kwargs)

    def resolved(self, **kwargs):
        return self.filter(status=TODO_STATUS.resolved, is_deleted=False).filter(**kwargs)

    def closed(self, **kwargs):
        return self.filter(status=TODO_STATUS.closed, is_deleted=False).filter(**kwargs)


class DefaultFeedbackRequestManager(models.Manager):
    def open(self, **kwargs):
        """
        Open Feedback Requests
        """
        return self.filter(status=FEEDBACK_STATUS.open).filter(**kwargs)

    def close_by_todo(self, todo):
        """
        Close FeedbackRequests that are open by a specific todo
        """
        closed_notice_message = 'Todo instance was set to closed. All open Feedback requests were therefor cancelled'
        self.open(attachment__in=todo.attachments.all()).update(status=FEEDBACK_STATUS.cancelled, comment=closed_notice_message)