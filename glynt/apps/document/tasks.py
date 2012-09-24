# -*- coding: utf-8 -*-
# tasks to handle the sending of signature invitations
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from templated_email import send_templated_mail
from celery.task import task

import user_streams


@task()
def document_created(**kwargs):
    """
    """
    # Send notification
    document = kwargs['document']
    doc_type = document.source_document.name
    user = document.owner
    user_streams.add_stream_item(user, _('You created a "%s" document "<a href="%s">%s</a>"' % (doc_type, document.get_absolute_url(), document.name,)))


@task()
def document_deleted(**kwargs):
    """
    """
    # Send notification
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Deleted the document "<a href="%s">%s</a>"' % (document.get_absolute_url(), document.name,)))


@task()
def document_restored(**kwargs):
    """
    """
    # Send notification
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Restored the deleted document "<a href="%s">%s</a>"' % (document.get_absolute_url(), document.name,)))


@task()
def document_cloned(**kwargs):
    """
    """
    # Send notification
    source_document = kwargs['source_document']
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Cloned the document "<a href="%s">%s</a>" as "<a href="%s">%s</a>"' % (source_document.get_absolute_url(), source_document.name, document.get_absolute_url(), document.name,)))

