# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from glynt.apps.document.models import ClientCreatedDocument

from glynt.apps.document.models import DocumentHTML
from glynt.apps.services import GlyntPdfService


import logging
logger = logging.getLogger(__name__)


class ExportAsPDFView(View):
    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document', 'source_document__flyform'), slug=self.kwargs['slug'], owner=request.user)
        document_html = get_object_or_404(DocumentHTML, document=document)

        filename = '%s.pdf' % (document.slug,)
        try:
            pdf_service = GlyntPdfService(html=document_html.render(), title=document.name)
            response = HttpResponse(pdf_service.create_pdf(), status=200, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s' % (filename,)
        except Exception as e:
            logger.error(e)
            response = HttpResponse('[{"message":"%s"}]' % (e,), status=401, content_type="text/json")

        return response
