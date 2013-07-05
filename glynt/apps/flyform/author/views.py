# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.generic.base import TemplateView
from django.views.generic.edit import BaseUpdateView

from glynt.apps.flyform.author.forms import CreateStepForm, CreateStepFieldForm, DocumentForm, DocumentMetaForm

import json
import logging
logger = logging.getLogger(__name__)

class Document(object):
    pass


class AuthorToolView(TemplateView, BaseUpdateView):
    template_name = 'author/authoring_tool.html'

    def get_context_data(self, **kwargs):
        context = {}

        context['form_steps'] = CreateStepForm()
        context['form_fields'] = CreateStepFieldForm()
        context['form_document'] = DocumentForm()
        context['form_document_meta'] = DocumentMetaForm()

        context['csrf_raw_token'] = get_token(self.request)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['object'].flyform.body = json.dumps(json.loads(request.POST.get('json')))
        context['object'].flyform.save()
        result = [{'pk':context['object'].pk}]
        return HttpResponse(json.dumps(result), status=200, content_type='text/json')
