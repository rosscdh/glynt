# -*- coding: utf-8 -*-
#import docraptor
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

import datetime
import hashlib

import logging
logger = logging.getLogger('django.request')


class BaseService(object):
    template = 'export/pdf.html'

    def __init__(self, html, **kwargs):
        self.html = html
        self.kwargs = kwargs

    def get_context(self):
        title = self.kwargs.get('title', None)
        html = smart_text(self.html, encoding='utf-8', strings_only=False, errors='strict')

        context = {
            'title': title
            ,'body': html
        }

        return context

    def get_html(self, context):
        # Render the core body wrapped in custom html
        return render_to_string(self.template, context)


class GlyntPdfService(BaseService):
    """
        PDF Creation Service
    """
    def create_pdf(self):
        context = self.get_context()

        logger.info('using GlyntDocxService Service to create .docx "%s"'%(context['title'],))

        html = self.get_html(context=context)

        # use the export wrapper HTML, to render the context
        pdf = StringIO.StringIO()
        try:
            pisa.CreatePDF(html.encode("UTF-8"), pdf , encoding='UTF-8', link_callback=link_callback)
        except Exception as e:
            logger.error('Could not generate PDF "%s" with pisa: "%s"'%(context['title'], e,))

        # return pdf pointer to 0 to allow reading into ContentFile
        pdf.seek(0)

        # return a ContentFile object to be used
        return ContentFile(pdf.read(), name=context['title'])


class GlyntDocxService(BaseService):
    """
        Docx Creation Service
    """
    def create_pdf(self):
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

