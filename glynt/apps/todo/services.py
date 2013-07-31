# coding: utf-8
"""
Service that abstract the various creation processes todos
"""
from django.conf import settings

import logging
logger = logging.getLogger('lawpal.services')

CROCDOC_API_KEY = getattr(settings, 'CROCDOC_API_KEY', None)
if CROCDOC_API_KEY is None:
    raise "You must specify a CROCDOC_API_KEY in your local_settings.py"

import crocodoc

crocodoc.api_token = CROCDOC_API_KEY


class CrocdocAttachmentService(object):
    attachment = None
    session = None
    def __init__(self, attachment, *args, **kwargs):
        self.attachment = attachment

    @property
    def uuid(self):
        if self.attachment.crocdoc_uuid is None:

            uuid = self.upload_document()

            crocdoc = self.attachment.data.get('crocdoc', {})
            crocdoc['uuid'] = uuid

            self.attachment.data['crocdoc'] = crocdoc
            self.attachment.save(update_fields=['data'])

            return uuid
        else:
            return self.attachment.crocdoc_uuid

    def session_key(self):
        if self.session is None:
            self.session = crocodoc.session.create(self.uuid)
        return self.session

    def upload_document(self):
        return crocodoc.document.upload(url=self.attachment.get_url())

    def view_url(self):
        return 'https://crocodoc.com/view/{session_key}'.format(session_key=self.session_key())

    def process(self):
        return self.uuid