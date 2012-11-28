# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import simplejson as json
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify


from glynt.apps.document.views import DocumentView
from glynt.apps.document.views.utils import user_can_view_document
from glynt.apps.document.models import Document, ClientCreatedDocument


class MyDocumentView(DocumentView):
    """ Used when viewing a users own documents """
    template_name='smoothe/document.html'
    def get_context_data(self, **kwargs):
        context = super(MyDocumentView, self).get_context_data(**kwargs)

        try:
            self.user_document = ClientCreatedDocument.objects.select_related('source_document').get(slug=self.document_slug, owner=self.request.user)
            invitee_list = self.user_document.documentsignature_set.all()
        except ClientCreatedDocument.DoesNotExist:
            self.user_document = None
            invitee_list = []

        context['userdoc'] = self.user_document
        context['object'] = self.document
        context['document'] = self.document.body

        return context