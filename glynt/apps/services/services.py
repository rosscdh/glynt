# -*- coding: utf-8 -*-
#import docraptor
from django.conf import settings
from glynt.apps.export.utils import fetch_resources as link_callback
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.files.storage import default_storage

from xhtml2pdf import pisa
import StringIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.utils.encoding import smart_unicode as smart_text # preparing for 1.5

from hellosign import HelloSign, HelloSignSignature
from hellosign import HelloSigner, HelloDoc

import datetime
import hashlib

import logging
logger = logging.getLogger('django.request')


class BaseService(object):
    def __init__(self, html, **kwargs):
        self.html = html
        self.kwargs = kwargs


class GlyntPdfService(BaseService):
    """
        PDF Creation Service
    """
    def create_pdf(self):
        title = self.kwargs.get('title', None)
        html = smart_text(self.html, encoding='utf-8', strings_only=False, errors='strict')
        logger.info('using GlyntPdfService Service to create "%s"'%(title,))

        context = {
            'title': title
            ,'body': html
        }

        # Render the core body wrapped in custom html
        html = render_to_string('export/pdf.html', context)

        # use the export wrapper HTML, to render the context
        pdf = StringIO.StringIO()
        try:
            pisa.CreatePDF(html.encode("UTF-8"), pdf , encoding='UTF-8', link_callback=link_callback)
        except Exception as e:
            logger.error('Could not generate PDF "%s" with pisa: "%s"'%(context['title'], e,))

        # return pdf pointer to 0 to allow reading into ContentFile
        pdf.seek(0)

        # return a ContentFile object to be used
        return ContentFile(pdf.read())


class HelloSignService(object):
    """
        Service that allows us to send a document for signing
    """
    def __init__(self, document, invitees, **kwargs):
        self.document = document
        logger.info('Submitting document to HelloSign: "%s"'%(document,))

        document_html = self.document.documenthtml_set.all()[0]
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
        m = hashlib.md5()
        m.update(str(datetime.datetime.now()))
        return '%s/%s-%s.pdf'%(settings.MEDIA_ROOT, self.document.pk, m.hexdigest(),)

    def send_for_signing(self):
        signature = HelloSignSignature(title=self.document.name, subject=self.subject, message=self.message)

        for i in self.invitees:
            signature.add_signer(HelloSigner(name=i['name'], email=i['email']))

        # Add the document to sign
        tmp_filename = self.random_filename()
        pdf = self.pdf_provider.create_pdf()
        # Save it temporarily
        path = default_storage.save(tmp_filename, pdf)
        logger.info('Saved document to: "%s"'%(path,))

        signature.add_doc(HelloDoc(file_path=path))

        # Perform the submission
        try:
            result = signature.create(auth=self.pdf_provider_authentication)
        except Exception as e:
            logger.error('Could not submit %s to HelloSign: "%s"'%(path, e,))

        # Delete the tmp file
        pdf.delete(save=False)

        return result


# class DocRaptorService(BaseService):
#     def create_pdf(self):
#         logger.info('using DocRaptor Service')
#         dr = docraptor.DocRaptor(api_key='LsEAKMvtz5hXBVAyfr')
# 
#         with open("/tmp/docraptor.pdf", "wb") as pdf:
#             pdf.write(dr.create({
#                 'document_content': self.html, 
#                 'test': True
#             }).content)
