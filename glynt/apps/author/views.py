# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.utils import simplejson as json
from django.views.generic.base import TemplateView
from django.views.generic.edit import BaseUpdateView


from glynt.apps.document.forms import CreateStepForm, CreateStepFieldForm
from glynt.apps.document.models import Document

import logging
logger = logging.getLogger(__name__)


class AuthorToolView(TemplateView, BaseUpdateView):
    template_name='author/authoring_tool.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorToolView, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            context['object'] = Document.objects.select_related('flyform').get(pk=self.kwargs['pk'])
            context['json'] = json.dumps(context['object'].flyform.body)

        context['form_steps'] = CreateStepForm()
        context['form_fields'] = CreateStepFieldForm()
        context['csrf_raw_token'] = get_token(self.request)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['object'].flyform.body = json.dumps(json.loads(request.POST.get('json')))
        result = context['object'].flyform.save()
        return HttpResponse(result, status=200, content_type='text/json')