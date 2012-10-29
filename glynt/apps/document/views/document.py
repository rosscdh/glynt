# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin

from utils import JsonErrorResponseMixin, user_can_view_document

from glynt.apps.flyform.forms import BaseFlyForm
from glynt.apps.document.views.utils import FORM_GROUPS
from glynt.apps.document.forms import ClientCreatedDocumentForm
from glynt.apps.document.models import Document

import logging
logger = logging.getLogger(__name__)


class DocumentView(TemplateView, FormMixin, JsonErrorResponseMixin):
  """ Default view of the document """
  def get_context_data(self, **kwargs):
    context = super(DocumentView, self).get_context_data(**kwargs)

    document_slug = slugify(self.kwargs['slug'])

    self.document = get_object_or_404(Document.objects.select_related('flyform'), slug=document_slug)

    context['csrf_raw_token'] = get_token(self.request)

    context['object'] = self.document
    context['document'] = self.document.body
    context['default_data'] = self.document.default_data_as_json()
    context['userdoc_form'] = ClientCreatedDocumentForm()

    try:
      context['form_set'] = self.document.flyform.flyformset()
    except KeyError:
      context['form_set'] = FORM_GROUPS['no_steps']

    user_can_view_document(self.document, self.request.user)

    return context

  def get_form_class(self):
    """
    Returns the form class to use in this view
    """
    return BaseFlyForm

  def get_form(self, form_class):
    """
    Returns an instance of the form to be used in this view.
    """
    kwargs = self.get_form_kwargs()

    self.step = int(self.request.GET.get('step', 0))
    if self.step > 0:
      self.step = self.step - 1

    kwargs['json_form'] = self.document.flyform.body[self.step]

    return form_class(**kwargs)

  def post(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)

    form_class = self.get_form_class()
    form = self.get_form(form_class)

    response = self.get_response_json(form)

    return HttpResponse(json.dumps(response), status=response['status'], content_type='text/json')


