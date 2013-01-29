# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

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
    user_streams.add_stream_item(user, _('You created a "%s" document "<a href="%s">%s</a>"' % (doc_type, document.get_absolute_url(), document.name,)), document)


@task()
def document_deleted(**kwargs):
    """
    """
    # Send notification
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Deleted the document "%s"' % (document.name,)), document)


@task()
def document_restored(**kwargs):
    """
    """
    # Send notification
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Restored the deleted document "<a href="%s">%s</a>"' % (document.get_absolute_url(), document.name,)), document)


@task()
def document_cloned(**kwargs):
    """
    """
    # Send notification
    source_document = kwargs['source_document']
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Cloned the document "<a href="%s">%s</a>" as "<a href="%s">%s</a>"' % (source_document.get_absolute_url(), source_document.name, document.get_absolute_url(), document.name,)), document)


@task()
def document_comment(**kwargs):
    """
    When a user Comments on a document
    """
    # Send notification
    document = kwargs['document']
    #source_document = kwargs['source_document']
    commenting_user = kwargs['commenting_user']
    commenting_user_name = kwargs['commenting_user_name']
    username = commenting_user.get_full_name() if commenting_user else commenting_user_name
    comment = kwargs['comment']
    user = document.owner
    user_streams.add_stream_item(user, _('%s commented on "<a href="%s">%s</a>" - "%s"' % (username, document.get_absolute_url(), document.name, comment,)), document)


@task()
def generate_document_html(**kwargs):
    document = kwargs['document']
    # extract source HTML
    # convert handlebars template tags
    # save to document.body