# -*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from glynt.apps.todo import TODO_STATUS


class DefaultToDoManager(models.Manager):
    def new(self, **kwargs):
        return self.filter(status=TODO_STATUS.new).filter(**kwargs)

    def open(self, **kwargs):
        return self.filter(status=TODO_STATUS.open).filter(**kwargs)

    def closed(self, **kwargs):
        return self.filter(status=TODO_STATUS.closed).filter(**kwargs)