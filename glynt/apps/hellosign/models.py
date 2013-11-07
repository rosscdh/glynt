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
    data = JSONField(default={})
    signature_request_id = models.CharField(max_length=255, db_index=True)
    is_complete = models.BooleanField(default=False, db_index=True)
