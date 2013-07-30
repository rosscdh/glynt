# coding: utf-8
"""
App to enable founders to have a set of todo items per transaction type
considering using https://github.com/bartTC/django-attachments for the
todo attachments when the time comes
"""
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from glynt.apps.utils import generate_unique_slug
from glynt.apps.project.models import Project

from django_filepicker.models import FPFileField

from . import TODO_STATUS
from .managers import DefaultToDoManager

from jsonfield import JSONField


def _attachment_upload_file(instance, filename):
    _, ext = os.path.splitext(filename)
    return '{project_uuid}/attachments/{slug}{ext}'.format(project_uuid=instance.project.uuid, slug=instance.slug, ext=ext)


class Attachment(models.Model):
    attachment = FPFileField(upload_to=_attachment_upload_file)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)


class ToDo(models.Model):
    """ ToDo Items that are associated with a user and perhaps with a project """
    user = models.ForeignKey(User, blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    category = models.CharField(max_length=128, db_index=True)
    description = models.TextField(blank=True, null=True)
    attachments = models.ManyToManyField(Attachment, related_name='attachments')
    status = models.IntegerField(choices=TODO_STATUS.get_choices(), default=TODO_STATUS.unassigned, db_index=True)
    data = JSONField(default={})
    date_due = models.DateTimeField(blank=True, null=True, auto_now=False, auto_now_add=False, db_index=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)

    objects = DefaultToDoManager()

    def __unicode__(self):
        return '{name}'.format(name=self.name)

    @property
    def todo_type(self):
        return '%s' % 'Generic' if not self.project else 'Need to hook up to project'

    @property
    def display_status(self):
        return TODO_STATUS.get_desc_by_value(self.status)

    @property
    def original_name(self):
        return self.data.get('name', 'No original name was found, was created by user')

    def get_absolute_url(self):
        return reverse('todo:edit', kwargs={'project_uuid': self.project.uuid, 'slug': self.slug})

    def save(self, *args, **kwargs):
        """ Ensure that we have a slug """
        if self.slug in [None, '']:
            self.slug = generate_unique_slug(instance=self)

        return super(ToDo, self).save(*args, **kwargs)
