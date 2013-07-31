# coding: utf-8
"""
Service that abstract the various creation processes todos
"""
from django.conf import settings

import logging
logger = logging.getLogger('lawpal.services')

CROCDOC_API_KEY = getattr(settings, 'CROCDOC_API_KEY', None)
if CROCDOC_API_KEY is None:
    raise Exception("You must specify a CROCDOC_API_KEY in your local_settings.py")

import crocodoc

crocodoc.api_token = CROCDOC_API_KEY


class CrocdocAttachmentService(object):
    attachment = None
    session = None
    def __init__(self, attachment, *args, **kwargs):
        logger.info('Init CrocdocAttachmentService.__init__ for attachment: {pk}'.format(pk=attachment.pk))
        self.attachment = attachment

    @property
    def uuid(self):
        if self.attachment.crocdoc_uuid is None:
            try:
                uuid = self.upload_document()
                logger.info('CrocdocAttachmentService.uuid: {uuid}'.format(uuid=uuid))
            except Exception as e:
                logger.error('CrocdocAttachmentService.uuid: Failed to Generate uuid'.format(uuid=uuid))
                raise e

            crocdoc = self.attachment.data.get('crocdoc', {})
            crocdoc['uuid'] = uuid

            self.attachment.data['crocdoc'] = crocdoc
            self.attachment.save(update_fields=['data'])

            return uuid
        else:
            return self.attachment.crocdoc_uuid

    def session_key(self, **kwargs):
        if self.session is None:
            self.session = crocodoc.session.create(self.uuid, **kwargs)
        return self.session

    def upload_document(self):
        url = self.attachment.get_url()
        logger.info('Upload file to crocdoc: {url}'.format(url=url))
        return crocodoc.document.upload(url=url)

    def view_url(self):
        url = 'https://crocodoc.com/view/{session_key}'.format(session_key=self.session_key())
        logger.info('provide crocdoc view_url: {url}'.format(url=url))
        return url

    def process(self):
        logger.info('Start CrocdocAttachmentService.process')
        return self.uuid