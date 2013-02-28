# -*- coding: utf-8 -*-
import os
from django.conf import settings
from glynt.apps.export.utils import fetch_resources as link_callback
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.files.storage import default_storage

from xhtml2pdf import pisa
import StringIO
import sh

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.utils.encoding import smart_unicode as smart_text # preparing for 1.5

from hellosign import HelloSign, HelloSignSignature
from hellosign import HelloSigner, HelloDoc

import docraptor
DOCRAPTOR_KEY = getattr(settings, 'DOCRAPTOR_KEY', None)

import datetime
import hashlib

import logging
logger = logging.getLogger('django.request')


class BasePdfService(object):
    template = 'export/pdf.html'

    def __init__(self, html, **kwargs):
        self.html = html
        self.kwargs = kwargs

        if 'template' in kwargs:
            self.template = kwargs.get('template')

    def get_context(self):
        title = self.kwargs.get('title', None)
        html = smart_text(self.html, encoding='utf-8', strings_only=False, errors='strict')

        context = {
            'title': title
            ,'body': html
        }

        return context

    def get_html(self, context=None):
        context = context if context is not None else self.get_context()
        # Render the core body wrapped in custom html
        return render_to_string(self.template, context)


class DocRaptorService(BasePdfService):
    def create_pdf(self):
        logger.info('using DocRaptor Service: %s' % DOCRAPTOR_KEY)
        context = self.get_context()
        title = context.get('title', 'Untitled Document')

        html = self.get_html(context=context)
        logger.debug('Local HTML Response: %s' % html)

        try:
            dr = docraptor.DocRaptor(api_key=DOCRAPTOR_KEY)

            pdf_response = dr.create({
                        'document_content': html.encode("UTF-8"),
                        'test': True
                    }).content

            logger.info('DocRaptor Response Type: %s' % type(pdf_response))
            if type(pdf_response) == str:
                logger.debug('DocRaptor Response: %s' % pdf_response)

        except Exception as e:
            logger.error(e)

        return ContentFile(pdf_response, name=title)


class XHTML2PdfService(BasePdfService):
    """
        PDF Creation Service
    """
    def create_pdf(self):
        context = self.get_context()
        title = context.get('title', 'Untitled Document')

        logger.info('using GlyntPdfService Service to create .pdf "%s"'%(title,))

        html = self.get_html(context=context)

        # use the export wrapper HTML, to render the context
        pdf = StringIO.StringIO()
        try:
            pisa.CreatePDF(html.encode("UTF-8"), pdf , encoding='UTF-8', link_callback=link_callback)
        except Exception as e:
            logger.error('Could not generate PDF "%s" with pisa: "%s"'%(title, e,))

        # return pdf pointer to 0 to allow reading into ContentFile
        pdf.seek(0)

        # return a ContentFile object to be used
        return ContentFile(pdf.read(), name=title)


class GlyntPdfService(DocRaptorService):
    """
        Interface to the various PDF Creation Services
        Used by the views
    """
    pass


class HelloSignService(object):
    """
        Service that allows us to send a document for signing
    """
    def __init__(self, document, invitees, **kwargs):
        self.document = document
        logger.info('Submitting document to HelloSign: "%s"'%(document.name,))

        document_html = self.document.documenthtml_set.all()[0]

        # Dependency injected class for testing
        self.HelloSignSignatureClass = kwargs.get('HelloSignSignatureClass', HelloSignSignature)

        self.invitees = invitees
        self.user = kwargs.get('user', None)
        self.subject = kwargs.get('subject', None)
        self.message = kwargs.get('message', None)

        try:
            self.pdf_provider_authentication = settings.HELLOSIGN_AUTH
        except AttributeError:
            logger.critical("No settings.HELLOSIGN_AUTH has been specified. Please provide them")

        self.pdf_provider = GlyntPdfService(html=document_html.render(), title=document.name)

    def random_filename(self):
        """
            Should return in the form: MEDIA_ROOT/:id-:md5hash.pdf
        """
        m = hashlib.md5()
        m.update(str(datetime.datetime.utcnow()))
        return '%s/%s-%s.pdf'%(settings.MEDIA_ROOT, self.document.pk, m.hexdigest(),)

    def send_for_signing(self):
        signature = self.HelloSignSignatureClass(title=self.document.name, subject=self.subject, message=self.message)

        # Add invitees
        for i in self.invitees:
            signature.add_signer(HelloSigner(name=i['name'], email=i['email']))

        # Add the document to sign
        tmp_filename = self.random_filename()
        pdf = self.pdf_provider.create_pdf()

        # Save it temporarily
        path = default_storage.save(tmp_filename, pdf)
        logger.info('Saved tmp document to: "%s"'%(path,))

        signature.add_doc(HelloDoc(file_path=path))

        # Perform the submission
        try:
            result = signature.create(auth=self.pdf_provider_authentication)
        except Exception as e:
            result = None
            logger.error('Could not submit %s to HelloSign: "%s"'%(path, e,))

        # Delete the tmp file
        default_storage.delete(path)
        logger.info('Deleted tmp document: "%s"'%(path,))

        return result
