# -*- coding: utf-8 -*-
"""
Tasks that will handle signals and events for todo and attachments
"""
from celery.task import task

import logging
logger = logging.getLogger('django.request')

from .services import CrocdocAttachmentService, InkFilePickerAttachmentService


@task()
def delete_attachment(is_new, attachment, **kwargs):
    """
    """
    if attachment:
        if attachment.crocdoc_uuid is not None:
            crocdoc_service = CrocdocAttachmentService(attachment=attachment, **kwargs)
            crocdoc_service.remove()

        if attachment.inkfilepicker_url is not None:
            inkfilepicker_service = InkFilePickerAttachmentService(attachment=attachment, **kwargs)
            inkfilepicker_service.remove()
