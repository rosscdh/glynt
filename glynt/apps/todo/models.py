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
from hurry.filesize import size


def _attachment_upload_file(instance, filename):
    _, ext = os.path.splitext(filename)
    return '{project_uuid}/attachments/{slug}{ext}'.format(project_uuid=instance.project.uuid, slug=instance.slug, ext=ext)


class ToDo(models.Model):
    TODO_STATUS_CHOICES = TODO_STATUS
    """ ToDo Items that are associated with a user and perhaps with a project """
    user = models.ForeignKey(User, blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    category = models.CharField(max_length=128, db_index=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=TODO_STATUS_CHOICES.get_choices(), default=TODO_STATUS_CHOICES.unassigned, db_index=True)
    data = JSONField(default={})
    date_due = models.DateTimeField(blank=True, null=True, auto_now=False, auto_now_add=False, db_index=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)

    objects = DefaultToDoManager()

    def __unicode__(self):
        return '{name}'.format(name=self.name)

    @property
    def pusher_id(self):
        return self.slug

    @property
    def todo_type(self):
        return '%s' % 'Generic' if not self.project else 'Need to hook up to project'

    @property
    def display_status(self):
        return self.TODO_STATUS_CHOICES.get_desc_by_value(self.status)

    @property
    def original_name(self):
        return self.data.get('name', 'No original name was found, was created by user')

    def get_absolute_url(self):
        return reverse('todo:edit', kwargs={'project_uuid': self.project.uuid, 'slug': self.slug})

    # def save(self, *args, **kwargs):
    #     """ Ensure that we have a slug """
    #     if self.slug in [None, '']:
    #         self.slug = generate_unique_slug(instance=self)

    #     return super(ToDo, self).save(*args, **kwargs)


class Attachment(models.Model):
    uuid = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    attachment = FPFileField(upload_to=_attachment_upload_file, additional_params=None)
    project = models.ForeignKey(Project, related_name='attachments')
    todo = models.ForeignKey(ToDo, blank=True, null=True, related_name='attachments')
    data = JSONField(default={})
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-date_created']

    @property
    def pusher_id(self):
        return self.todo.pusher_id

    @property
    def filename(self):
        return self.data.get('fpfile', {}).get('filename')

    @property
    def mimetype(self):
        return self.data.get('fpfile', {}).get('mimetype')

    @property
    def size(self):
        return size(self.data.get('fpfile', {}).get('size', 0))

    @property
    def crocdoc_uuid(self):
        return self.data.get('crocdoc', {}).get('uuid')

    @property
    def inkfilepicker_url(self):
        return self.data.get('fpfile', {}).get('url')

    @property
    def s3_key(self):
        return self.data.get('fpfile', {}).get('key')

    def get_url(self):
        return self.attachment.name

"""
import signals
"""
from glynt.apps.todo.signals import (on_attachment_created, on_attachment_deleted, on_comment_created)
