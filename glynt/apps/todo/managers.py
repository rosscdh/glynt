# -*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from glynt.apps.todo import TODO_STATUS


class DefaultToDoManager(models.Manager):
    def open(self, **kwargs):
        self.filter(status=TODO_STATUS.open).filter(**kwargs)

    def done(self, **kwargs):
        self.filter(status=TODO_STATUS.done).filter(**kwargs)

    def in_progress(self, **kwargs):
        self.filter(status=TODO_STATUS.new).filter(**kwargs)
