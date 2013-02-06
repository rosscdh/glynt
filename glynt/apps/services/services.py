# -*- coding: utf-8 -*-
#import docraptor

from glynt.apps.export.utils import fetch_resources as link_callback
from django.template import RequestContext
from django.template.loader import render_to_string

from xhtml2pdf import pisa
import StringIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.utils.encoding import smart_unicode as smart_text # preparing for 1.5

from hellosign import HelloSign, HelloSignSignature
from hellosign import HelloSigner, HelloDoc

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
        logger.info('using GlyntPdfService Service')

        title = self.kwargs.get('title', None)
        html = smart_text(self.html, encoding='utf-8', strings_only=False, errors='strict')

        context = {
            'title': title
            ,'body': html
        }

        # Render the core body wrapped in custom html
        html = render_to_string('export/pdf.html', context)

        # use the export wrapper HTML, to render the context
        pdf = StringIO.StringIO()
        pisa.CreatePDF(html.encode("UTF-8"), pdf , encoding='UTF-8', link_callback=link_callback)
        pdf.seek(0)

        # return a contentfile object to be used
        return ContentFile(pdf.read())


class HelloSignService(object):
    """
        Service that allows us to send a document for signing
    """
    def __init__(self, document, invitees, **kwargs):
        self.document = document

        document_html = self.document.documenthtml_set.all()[0]
        self.invitees = invitees
        self.user = kwargs.get('user', None)
        self.subject = kwargs.get('subject', None)
        self.message = kwargs.get('message', None)

        self.pdf_provder_authentication = ("sendrossemail@gmail.com", "zanshin77")
        self.pdf_provder = GlyntPdfService(html=document_html.render(), title=document.name)

    def send_for_signing(self):
        signature = HelloSignSignature(title=self.document.name, subject=self.subject, message=self.message)

        for i in self.invitees:
            signature.add_signer(HelloSigner(name=i['name'], email=i['email']))

        # Add the document to sign
        signature.add_doc(HelloDoc(file_path=self.pdf_provder.create_pdf()))

        return signature.create(auth=self.pdf_provder_authentication)


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
