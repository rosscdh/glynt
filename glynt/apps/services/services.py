import docraptor
import pdfcrowd

import logging
logger = logging.getLogger('django.request')


class BaseService(object):
    def __init__(self, html, **kwargs):
        self.html = html


class DocRaptorService(BaseService):
    def create_pdf(self):
        logger.info('using DocRaptor Service')
        dr = docraptor.DocRaptor(api_key='LsEAKMvtz5hXBVAyfr')

        with open("/tmp/docraptor.pdf", "wb") as pdf:
            pdf.write(dr.create({
                'document_content': self.html, 
                'test': True
            }).content)


class PdfCrowdService(BaseService):
    def create_pdf(self):
        logger.info('using PDFCrowd Service')
        client = pdfcrowd.Client("rossc", "77862631d91bd3ff79f2cc7a91fb5eaf")
        output_file = open("/tmp/pdfcrowd.pdf", 'wb')
        client.convertHtml(self.html, output_file)
        output_file.close()
