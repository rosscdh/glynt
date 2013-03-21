# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.template.defaultfilters import slugify

from glynt.apps.document.models import ClientCreatedDocument
from glynt.apps.document.models import DocumentHTML
from glynt.apps.services import GlyntPdfService, GlyntDocService
from glynt.apps.services.services import BaseDocumentAssemblerService


import logging
logger = logging.getLogger('django.request')


class ExportAsPDFView(View):
    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document', 'source_document__flyform'), pk=self.kwargs['pk'])
        document_html = get_object_or_404(DocumentHTML, document=document)

        filename = '%s.pdf' % slugify(document.name)

        try:
            pdf_service = GlyntPdfService(document=document, html=document_html.render(), title=document.name)

            response = HttpResponse(pdf_service.create_pdf(), status=200, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s' % (filename,)
        except Exception as e:
            logger.error(e)
            response = HttpResponse('[{"message":"%s"}]' % (e,), status=401, content_type="text/json")

        return response


class ExportAsDOCView(View):
    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document', 'source_document__flyform'), pk=self.kwargs['pk'])
        document_html = get_object_or_404(DocumentHTML, document=document)

        filename = '%s.docx' % slugify(document.name)

        try:
            doc_service = GlyntDocService(document=document, html=document_html.render(), title=document.name)

            response = HttpResponse(doc_service.create_doc(), status=200, content_type='application/docx')
            response['Content-Disposition'] = 'attachment; filename=%s' % (filename,)
        except Exception as e:
            logger.error(e)
            response = HttpResponse('[{"message":"%s"}]' % (e,), status=401, content_type="text/json")

        return response


class ExportAsHTMLView(View):
    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document', 'source_document__flyform'), pk=self.kwargs['pk'])
        document_html = get_object_or_404(DocumentHTML, document=document)

        filename = '%s.html' % slugify(document.name)

        try:
            html_service = BaseDocumentAssemblerService(document=document, html=document_html.render(), title=document.name)

            response = HttpResponse(html_service.get_html(), status=200, content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename=%s' % (filename,)
        except Exception as e:
            logger.error(e)
            response = HttpResponse('[{"message":"%s"}]' % (e,), status=401, content_type="text/json")

        return response
