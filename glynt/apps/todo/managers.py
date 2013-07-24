# -*- coding: UTF-8 -*-
from django.db import models
from glynt.apps.todo import TODO_STATUS


class DefaultToDoManager(models.Manager):
    def unassigned(self, **kwargs):
        return self.filter(status=TODO_STATUS.unassigned).filter(**kwargs)

    def assigned(self, **kwargs):
        return self.filter(status=TODO_STATUS.assigned).filter(**kwargs)

    def closed(self, **kwargs):
        return self.filter(status=TODO_STATUS.closed).filter(**kwargs)