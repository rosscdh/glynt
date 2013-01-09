# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import simplejson as json
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.middleware.csrf import get_token
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse

from glynt.apps.document.views import DocumentView
from glynt.apps.document.views.utils import user_can_view_document
from glynt.apps.document.models import Document, ClientCreatedDocument

from .forms import DocumentForm as DocumentTemplateForm, ClientDocumentForm


class CreateDocumentView(CreateView):
    """ Create a new User Document from a Template """
    model = ClientCreatedDocument
    template_name='smoothe/document.html'

    def get_context_data(self, **kwargs):
        context = super(CreateDocumentView, self).get_context_data(**kwargs)

        invitee_list = []
        self.user_document = None
        self.document = get_object_or_404(Document, slug=self.kwargs['slug'])

        context['csrf_raw_token'] = get_token(self.request)
        context['submit_url'] = reverse('doc:create_document', kwargs={'slug': self.document.slug})
        context['object'] = self.document
        context['document'] = self.document.body
        context['default_data'] = self.document.default_data_as_json()
        context['userdoc'] = self.user_document
        context['object'] = self.document
        context['document'] = self.document.body

        return context


class UpdateDocumentView(UpdateView):
    """ Edit a User Document """
    model = ClientCreatedDocument
    template_name='smoothe/document.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateDocumentView, self).get_context_data(**kwargs)

        self.user_document = ClientCreatedDocument.objects.select_related('source_document').get(pk=self.pk)
        invitee_list = self.user_document.documentsignature_set.all()

        context['csrf_raw_token'] = get_token(self.request)
        context['submit_url'] = reverse('doc:update_document', kwargs={'pk': self.user_document.pk})
        context['userdoc'] = self.user_document
        context['object'] = self.document
        context['document'] = self.document.body

        return context


class CreateTemplateView(CreateView):
    """ Used creating a new document """
    template_name = 'smoothe/document-create.html'
    form_class = DocumentTemplateForm
    model = Document

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = self.initial.copy()
        initial.update({'owner': self.request.user})

        return initial

    def get_context_data(self, **kwargs):
      context = super(CreateDocumentView, self).get_context_data(**kwargs)

      self.document = context['form'].instance

      context['csrf_raw_token'] = get_token(self.request)

      context['object'] = self.document
      context['document'] = self.document.body
      context['default_data'] = None
      context['form'] = self.get_form(self.get_form_class())

      return context
