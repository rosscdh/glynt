# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

from jsonfield import JSONField

import urllib


class Signature(models.Model):
    """
    Model to store the HelloSign signature request
    """
    requested_by = models.ForeignKey('auth.User')
    signatories = models.ManyToManyField('auth.User', related_name='signatories')
    document = models.ForeignKey('todo.Attachment')
    data = JSONField(default={}, blank=True)
    signature_request_id = models.CharField(max_length=255, blank=True, db_index=True)
    is_complete = models.BooleanField(default=False, db_index=True)

    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def __unicode__(self):
        return u'{requested_by} requested signatures for {document} ({signature_request_id})'.format(requested_by=self.requested_by.get_full_name(), document=self.document, signature_request_id=self.signature_request_id)

    @property
    def subject(self):
        return self.data.get('subject')

    @subject.setter
    def subject(self, value):
        self.data['subject'] = value

    @property
    def message(self):
        return self.data.get('message')

    @message.setter
    def message(self, value):
        self.data['message'] = value

    @property
    def details_url(self):
        params = urllib.urlencode({'client_id': settings.HELLOSIGN_CLIENT_ID})
        return '{base}&{params}'.format(base=self.data.get('details_url'), params=params)

    @property
    def signing_url(self):
        params = urllib.urlencode({'client_id': settings.HELLOSIGN_CLIENT_ID})
        return '{base}&{params}'.format(base=self.data.get('signing_url'), params=params)


from .signals import on_signature_created