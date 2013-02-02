# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from celery.task import task
from glynt.apps.document.models import DocumentHTML
from glynt.apps.smoothe.pybars_smoothe import Smoothe
from glynt.apps.services import SaasposeService, DocRaptorService, PdfCrowdService

import user_streams

import logging
logger = logging.getLogger('django.request')


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

    # Get or create the HTML object
    html, is_new = DocumentHTML.objects.get_or_create(document=document)

    # convert handlebars template tags
    smoothe = Smoothe(source_html=document.body)

    try:
        html.html = smoothe.render(document.doc_data)
        html.save()
        # Send for HTML to PDF conversion
        convert_to_pdf(document_html=html)
    except Exception as e:
        logger.error('Could not save HTML for Document(%d): Exception: %s'%(document.pk, e,))


@task()
def convert_to_pdf(document_html, **kwargs):
    logger.info('Converting htmlto PDF Services')
    sp = SaasposeService(html=document_html.render())
    sp.create_pdf()

    # dr = DocRaptorService(html=document_html.render())
    # dr.create_pdf()

    # pc = PdfCrowdService(html=document_html.render())
    # pc.create_pdf()
