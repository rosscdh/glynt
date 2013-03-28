# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

from django_rq import job

from glynt.apps.document.models import DocumentHTML
from glynt.apps.services.services import GlyntPdfService, GlyntDocService

from glynt.apps.smoothe.pybars_smoothe import SmootheRemoval

from .services import HtmlValidatorService
from glynt.apps.smoothe.services import SmootheValidateService

import user_streams

import logging
logger = logging.getLogger('django.request')


@job()
def validate_document_html(ident, html):
    html_validator = HtmlValidatorService(ident=ident, html=html, preprocessors=[SmootheRemoval])
    smoothe_validator = SmootheValidateService(ident=ident, html=html)

    if not html_validator.is_valid():
        logger.warning(html_validator.error_msg)
        raise ValidationError(html_validator.error_msg)

    if not smoothe_validator.is_valid():
        logger.warning(smoothe_validator.error_msg)
        raise ValidationError(smoothe_validator.error_msg)


@job()
def document_created(**kwargs):
    """
    """
    # Send notification
    document = kwargs['document']
    doc_type = document.source_document.name
    user = document.owner
    user_streams.add_stream_item(user, _('You created a "%s" document "<a href="%s">%s</a>"' % (doc_type, document.get_absolute_url(), document.name,)), document)


@job()
def document_deleted(**kwargs):
    """
    """
    # Send notification
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Deleted the document "%s"' % (document.name,)), document)


@job()
def document_restored(**kwargs):
    """
    """
    # Send notification
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Restored the deleted document "<a href="%s">%s</a>"' % (document.get_absolute_url(), document.name,)), document)


@job()
def document_cloned(**kwargs):
    """
    """
    # Send notification
    source_document = kwargs['source_document']
    document = kwargs['document']
    user = document.owner
    user_streams.add_stream_item(user, _('You Cloned the document "<a href="%s">%s</a>" as "<a href="%s">%s</a>"' % (source_document.get_absolute_url(), source_document.name, document.get_absolute_url(), document.name,)), document)


@job()
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


@job()
def generate_document_html(**kwargs):
    document = kwargs['document']
    # Get or create the HTML object
    html, is_new = DocumentHTML.objects.get_or_create(document=document)
    # Only create the HTML if we dont have it already (derive from source document)
    if is_new is True:
        logger.info('Saving DocumentHTML document: %s'%(document.pk,))
        try:
            html.html = document.body
            html.save()
        except Exception as e:
            logger.error('Could not save HTML for Document(%d): Exception: %s'%(document.pk, e,))
    else:
        logger.info('DocumentHTML already exists document: %s'%(document.pk,))


@job()
def convert_to_pdf(document_html, **kwargs):
    """ 
        @TODO this is a POC
        >>> # Send for HTML to PDF conversion
        >>> convert_to_pdf(document_html=html, title=document.name)
    """
    logger.info('Creating PDF Document: %s DocumentHTML: %s'%(kwargs.get('document_pk', None), kwargs.get('document_html_pk', None),))
    glynt_pdf = GlyntPdfService(html=document_html.render(), title=kwargs.get('title', None))
    default_storage.save('%s/glyntpdf.pdf'%(settings.MEDIA_ROOT,), glynt_pdf.create_pdf())


@job()
def convert_to_doc(document_html, **kwargs):
    """ 
        @TODO this is a POC
        >>> # Send for HTML to DOCx conversion
        >>> convert_to_doc(document_html=html, title=document.name)
    """
    logger.info('Creating Docx Document: %s DocumentHTML: %s'%(kwargs.get('document_pk', None), kwargs.get('document_html_pk', None),))
    glynt_doc = GlyntDocService(html=document_html.render(), title=kwargs.get('title', None))
    default_storage.save('%s/glyntdoc.docx'%(settings.MEDIA_ROOT,), glynt_doc.create_doc())
