# coding: utf-8
"""
Service that abstract the various creation processes todos
"""
from django.conf import settings

from boto.s3.connection import S3Connection

import logging
logger = logging.getLogger('lawpal.services')

import crocodoc
import requests

FILEPICKER_API_KEY = getattr(settings, 'FILEPICKER_API_KEY', None)
if FILEPICKER_API_KEY is None:
    raise Exception('You must specify a FILEPICKER_API_KEY in your local_settings.py')

CROCDOC_API_KEY = getattr(settings, 'CROCDOC_API_KEY', None)
if CROCDOC_API_KEY is None:
    raise Exception("You must specify a CROCDOC_API_KEY in your local_settings.py")

AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
AWS_FILESTORE_BUCKET = getattr(settings, 'AWS_FILESTORE_BUCKET', None)

if AWS_ACCESS_KEY_ID is None:
    raise Exception("You must specify a AWS_ACCESS_KEY_ID in your local_settings.py")
if AWS_SECRET_ACCESS_KEY is None:
    raise Exception("You must specify a AWS_SECRET_ACCESS_KEY in your local_settings.py")
if AWS_FILESTORE_BUCKET is None:
    raise Exception("You must specify a AWS_FILESTORE_BUCKET in your local_settings.py")

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

            self.attachment.uuid = uuid

            self.attachment.data['crocdoc'] = crocdoc
            self.attachment.save(update_fields=['uuid', 'data'])

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

    def remove(self):
        # delete from crocdoc based on uuid
        deleted = crocodoc.document.delete(self.attachment.crocdoc_uuid)
        if deleted:
            logger.info('Deleted crocdoc file: {pk} - {uuid}'.format(pk=self.attachment.pk, uuid=self.attachment.crocdoc_uuid))
        else:
            logger.error('Could not Delete crocdoc file: {pk} - {uuid}'.format(pk=self.attachment.pk, uuid=self.attachment.crocdoc_uuid))

    def process(self):
        logger.info('Start CrocdocAttachmentService.process')
        return self.uuid


class InkFilePickerAttachmentService(object):
    def __init__(self, attachment, *args, **kwargs):
        logger.info('Init InkFilePickerAttachmentService.__init__ for attachment: {pk}'.format(pk=attachment.pk))
        self.attachment = attachment

    def remove(self):
        try:
            self.remove_from_inkfilepicker()
        except Exception as e:
            logger.error('InkFilePickerAttachmentService: Could not Delete inkfilepicker file: {pk} Error: {error}'.format(pk=self.attachment.pk, error=e))

        try:
            self.remove_from_s3()
        except Exception as e:
            logger.error('InkFilePickerAttachmentService: Could not Delete s3 file: {pk} Error: {error}'.format(pk=self.attachment.pk, error=e))

    def remove_from_inkfilepicker(self):
        url = self.attachment.inkfilepicker_url
        if url:
            r = requests.delete(url, params={'key': FILEPICKER_API_KEY})
            logger.info('InkFilePickerAttachmentService.remove_from_inkfilepicker for attachment: {pk} - to: {url} response ({status_code}): {response}'.format(pk=self.attachment.pk, url=r.url, response=r, status_code=r.status_code))

    def remove_from_s3(self):
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(AWS_FILESTORE_BUCKET)
        r = bucket.delete_key(self.attachment.s3_key)
        logger.info('InkFilePickerAttachmentService.remove_from_s3 for attachment: {pk} - to: {s3_key}, Response: {r}'.format(pk=self.attachment.pk, s3_key=self.attachment.s3_key, r=r))
