# -*- coding: UTF-8 -*-
from django.db import models
from glynt.apps.todo import TODO_STATUS


class DefaultToDoManager(models.Manager):
    def deleted(self, **kwargs):
        return self.filter(status=TODO_STATUS.new).filter(is_deleted=True, **kwargs)

    def new(self, **kwargs):
        return self.filter(status=TODO_STATUS.new).filter(**kwargs)

    def open(self, **kwargs):
        return self.filter(status=TODO_STATUS.open).filter(**kwargs)

    def pending(self, **kwargs):
        return self.filter(status=TODO_STATUS.pending).filter(**kwargs)

    def resolved(self, **kwargs):
        return self.filter(status=TODO_STATUS.resolved).filter(**kwargs)

    def closed(self, **kwargs):
        return self.filter(status=TODO_STATUS.closed).filter(**kwargs)
