# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from glynt.apps.document.models import ClientCreatedDocument
from glynt.apps.document import tasks

from glynt.pybars_plus import PybarsPlus

from django.template import RequestContext
from django_xhtml2pdf.utils import fetch_resources

import markdown
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO

import logging
logger = logging.getLogger(__name__)


class ExportAsPDFView(View):
    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        document_slug = slugify(self.kwargs['slug'])
        document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document', 'source_document__flyform'), slug=document_slug, owner=request.user)

        # @TODO Move all of this into a model method on ClientCreatedDocument
        data = []
        if type(document.source_document.flyform.defaults) is dict:
            data = document.source_document.flyform.defaults.items()
        if type(document.data) is dict:
            data = data + document.data.items()
            data = dict(data)
        if 'document_title' in data:
            data['document_title'] = document.name
        else:
            data['document_title'] = ''

        pybars_plus = PybarsPlus(document.body)
        body = pybars_plus.render(data)
        handlebars_template_body = mark_safe(markdown.markdown(body))

        context = RequestContext(request, {
            'body': handlebars_template_body
        })
        html = render_to_string('export/pdf.html', context)

        filename = '%s.pdf' % (document_slug,)
        pdf = StringIO.StringIO()
        result = pisa.CreatePDF(StringIO.StringIO(html.encode("UTF-8")), pdf, encoding='UTF-8', link_callback=fetch_resources)

        if result.err:
            response = HttpResponse('[{"message":"%s"}]' % (pdf.err,), status=401, content_type="text/json")
        else:
            response = HttpResponse(pdf.getvalue(), status=200, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s' % (filename,)
            return response

        return response
