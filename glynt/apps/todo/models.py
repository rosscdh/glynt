# -*- coding: UTF-8 -*-
"""
App to enable founders to have a set of todo items per transaction type
considering using https://github.com/bartTC/django-attachments for the
todo attachments when the time comes
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User
# from glynt.apps.project.models import Project

from django_filepicker.models import FPFileField


from glynt.apps.todo import TODO_STATUS, FEEDBACK_STATUS
from glynt.apps.todo.managers import (DefaultToDoManager,
                                      DefaultFeedbackRequestManager)
from .mixins import NumAttachmentsMixin

from rulez import registry

from jsonfield import JSONField
from hurry.filesize import size


def _attachment_upload_file(instance, filename):
    import os
    _, ext = os.path.splitext(filename)
    return '{project_uuid}/attachments/{slug}{ext}'.format(project_uuid=instance.project.uuid, slug=instance.pk, ext=ext)


class ToDo(NumAttachmentsMixin, models.Model):
    """
    ToDo Items that are associated with a project
    """
    TODO_STATUS_CHOICES = TODO_STATUS

    user = models.ForeignKey('auth.User', blank=True, null=True)
    project = models.ForeignKey('project.Project', blank=True, null=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField() # inherited from the .yml list based on project_id and other mixins
    category = models.CharField(max_length=128, db_index=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=TODO_STATUS.get_choices(), default=TODO_STATUS.new, db_index=True)
    data = JSONField(default={})
    date_due = models.DateTimeField(blank=True, null=True, auto_now=False, auto_now_add=False, db_index=True)

    sort_position = models.IntegerField(db_index=True, blank=True, null=True)
    sort_position_by_cat = models.IntegerField(db_index=True, blank=True, null=True)
    item_hash_num = models.CharField(max_length=24, db_index=True, blank=True, null=True)

    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = DefaultToDoManager()

    class Meta:
        ordering = ['sort_position']  # Maintain the sort order defined in yml

    def __unicode__(self):
        return u'{name}'.format(name=unicode(self.name))

    @staticmethod
    def content_type():
        """
        Static method used to access the content type of projects
        """
        return ContentType.objects.get_for_model(ToDo)

    @property
    def content_type_id(self):
        return ToDo.content_type().pk

    def can_read(self, user):
        return self.project.can_read(user=user)

    def can_edit(self, user):
        return self.project.can_edit(user=user)

    def can_delete(self, user):
        return self.project.can_delete(user=user)

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

    @property
    def item_hash_num(self):
        return '#{primary}-{secondary}'.format(primary=int(self.data.get('sort_position', 0)), secondary=int(self.data.get('sort_position_by_cat', 0)))

    def get_absolute_url(self):
        # need to import this HERE for some reason?
        from django.core.urlresolvers import reverse
        return reverse('todo:edit', kwargs={'project_uuid': self.project.uuid, 'slug': self.slug})

registry.register("can_read", ToDo)
registry.register("can_edit", ToDo)
registry.register("can_delete", ToDo)


class Attachment(models.Model):
    """
    Files that can be attached to our todo items
    """
    uuid = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    uploaded_by = models.ForeignKey('auth.User', related_name='atatchments_uploaded')
    deleted_by = models.ForeignKey('auth.User', blank=True, null=True, related_name='atatchments_deleted')
    attachment = FPFileField(upload_to=_attachment_upload_file, additional_params=None)
    project = models.ForeignKey('project.Project', related_name='attachments')
    todo = models.ForeignKey('todo.ToDo', blank=True, null=True, related_name='attachments')
    data = JSONField(default={})
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return u'{filename} {mimetype} ({size})'.format(filename=self.filename, mimetype=self.mimetype, size=0)

    def can_read(self, user):
        return self.project.can_read(user=user)

    def can_edit(self, user):
        return self.project.can_edit(user=user)

    def can_delete(self, user):
        return self.project.can_delete(user=user)

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

registry.register("can_read", Attachment)
registry.register("can_edit", Attachment)
registry.register("can_delete", Attachment)


class FeedbackRequest(models.Model):
    """ Feedback Request is used to associate requests for feedback 
    from a user on an attachment; is the primary mechanisim to obtain
    a response from a user on an attachment """
    FEEDBACK_STATUS_CHOICES = FEEDBACK_STATUS

    attachment = models.ForeignKey('todo.Attachment')
    assigned_by = models.ForeignKey('auth.User', related_name='requestedfeedback')
    assigned_to = models.ManyToManyField('auth.User', related_name='feedbackrequested')
    comment = models.CharField(max_length=255)
    status = models.IntegerField(choices=FEEDBACK_STATUS.get_choices(), default=FEEDBACK_STATUS.open, db_index=True)
    data = JSONField(default={})
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)

    objects = DefaultFeedbackRequestManager()

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        return u'{display_status} by: {assigned_by}'.format(display_status=self.display_status, assigned_by=self.assigned_by.get_full_name())

    def can_read(self, user):
        return self.attachment.project.can_read(user=user)

    def can_edit(self, user):
        return self.attachment.project.can_edit(user=user)

    def can_delete(self, user):
        return self.attachment.project.can_delete(user=user)

    @property
    def display_status(self):
        return self.FEEDBACK_STATUS_CHOICES.get_desc_by_value(self.status)

    @property
    def primary_assigned_to(self):
        try:
            return self.assigned_to.all()[0]
        except IndexError:
            return {}
