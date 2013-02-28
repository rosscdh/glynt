# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse

from glynt.apps.document.models import DocumentTemplate, ClientCreatedDocument
from glynt.apps.utils import AjaxableResponseMixin

from .forms import DocumentTemplateForm, ClientDocumentForm

import logging
logger = logging.getLogger(__file__)


class CreateTemplateView(AjaxableResponseMixin, CreateView):
    """ Used creating a new document template """
    template_name = 'smoothe/template-create.html'
    form_class = DocumentTemplateForm
    model = DocumentTemplate

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = self.initial.copy()
        initial.update({'owner': self.request.user})

        return initial

    def get_context_data(self, **kwargs):
      context = super(CreateTemplateView, self).get_context_data(**kwargs)

      self.document = context['form'].instance

      context['csrf_raw_token'] = get_token(self.request)

      context['object'] = self.document
      context['document'] = self.document.body
      context['default_data'] = None
      context['form'] = self.get_form(self.get_form_class())

      return context


class UpdateTemplateView(AjaxableResponseMixin, UpdateView):
    template_name = 'smoothe/template-edit.html'
    form_class = DocumentTemplateForm
    model = DocumentTemplate


class CreateDocumentView(AjaxableResponseMixin, CreateView):
    """ Create a new User Document from a Template """
    model = ClientCreatedDocument
    form_class = ClientDocumentForm
    template_name='smoothe/document.html'

    def get_form_kwargs(self):
        kwargs = super(CreateDocumentView, self).get_form_kwargs()
        self.document_template = get_object_or_404(DocumentTemplate, pk=self.kwargs['pk'])

        kwargs.update({
         'request': self.request,
         'source_document': self.document_template
        })

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateDocumentView, self).get_context_data(**kwargs)

        context['csrf_raw_token'] = get_token(self.request)
        context['submit_url'] = reverse('doc:create_document', kwargs={'pk': self.document_template.pk})
        context['document_template'] = self.document_template

        return context


class UpdateDocumentView(AjaxableResponseMixin, UpdateView):
    """ Edit a User Document """
    model = ClientCreatedDocument
    form_class = ClientDocumentForm
    template_name='smoothe/document.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateDocumentView, self).get_context_data(**kwargs)

        context['csrf_raw_token'] = get_token(self.request)
        context['submit_url'] = reverse('doc:update_document', kwargs={'pk': self.object.pk})
        context['document_template'] = self.object.source_document
        context['document_body'] = self.object.documenthtml_set.all()[0]

        return context


