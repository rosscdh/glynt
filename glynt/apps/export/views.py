# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import RequestContext

from glynt.apps.document.models import ClientCreatedDocument
from glynt.apps.export.utils import generate_pdf_template_object


import logging
logger = logging.getLogger(__name__)


class ExportAsPDFView(View):
    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document', 'source_document__flyform'), slug=self.kwargs['slug'], owner=request.user)

        filename = '%s.pdf' % (document.slug,)
        context = RequestContext(request, {
            'title': document.name,
            'body': document.rendered_body()
        })

        # try:
        result = generate_pdf_template_object(render_to_string('export/pdf.html', context))
        response = HttpResponse(result.getvalue(), status=200, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % (filename,)
        # except Exception as e:
        #     logger.error(e)
        #     print e
        #     response = HttpResponse('[{"message":"%s"}]' % (e,), status=401, content_type="text/json")

        return response
