# coding: utf-8
"""
App to enable founders to have a set of todo items per transaction type
considering using https://github.com/bartTC/django-attachments for the
todo attachments when the time comes
"""
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

from glynt.apps.todo import TODO_STATUS
from glynt.apps.todo.managers import DefaultToDoManager

from glynt.apps.engagement.models import Engagement


class ToDo(models.Model):
    """ ToDo Items that are associated with a user and perhaps with an engagement """
    user = models.ForeignKey(User)
    engagement = models.ForeignKey(Engagement, blank=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=TODO_STATUS.get_choices(), default=TODO_STATUS.open, db_index=True)
    data = JSONField(default={})
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    date_modified = models.DateField(auto_now=True, auto_now_add=True, db_index=True)

    objects = DefaultToDoManager()