# -*- coding: utf-8 -*-
from django.db import models
from jsonfield import JSONField


class Signature(models.Model):
    """
    Model to store the HelloSign signature request
    """
    requested_by = models.ForeignKey('auth.User')
    signatories = models.ManyToManyField('auth.User', related_name='signatories')
    project = models.ForeignKey('project.Project')
    data = JSONField(default={}, blank=True)
    signature_request_id = models.CharField(max_length=255, blank=True, db_index=True)
    is_complete = models.BooleanField(default=False, db_index=True)

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
        return self.data.get('details_url')

    @property
    def signing_url(self):
        return self.data.get('signing_url')