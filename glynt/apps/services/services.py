# -*- coding: utf-8 -*-
#import docraptor
#import pdfcrowd

from glynt.apps.export.utils import fetch_resources as link_callback
from django.template import RequestContext
from django.template.loader import render_to_string

from xhtml2pdf import pisa
import StringIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.utils.encoding import smart_unicode as smart_text # preparing for 1.5

import logging
logger = logging.getLogger('django.request')


class BaseService(object):
    def __init__(self, html, **kwargs):
        self.html = html
        self.kwargs = kwargs


class GlyntPdfService(BaseService):
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
# 
# 
# class PdfCrowdService(BaseService):
#     def create_pdf(self):
#         logger.info('using PDFCrowd Service')
#         client = pdfcrowd.Client("rossc", "77862631d91bd3ff79f2cc7a91fb5eaf")
#         output_file = open("/tmp/pdfcrowd.pdf", 'wb')
#         client.convertHtml(self.html, output_file)
#         output_file.close()
