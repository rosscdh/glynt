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

        document_slug = slugify(self.kwargs['slug'])

        try:
            self.user_document = ClientCreatedDocument.objects.select_related('source_document').get(slug=document_slug, owner=self.request.user)
            # Setup the document based on teh source_document of the viewed doc
            self.document = self.user_document.source_document
            invitee_list = self.user_document.documentsignature_set.all()
        except ClientCreatedDocument.DoesNotExist:
            self.user_document = None
            # Setup the document based on the source_document of the viewed doc
            self.document = Document.objects.get(slug=document_slug)
            invitee_list = []

        user_can_view_document(self.user_document, self.request.user)

        context['userdoc'] = self.user_document
        context['object'] = self.document
        context['document'] = self.document.body
        context['default_data'] = self.user_document.data_as_json() if self.user_document else self.document.default_data_as_json()
        context['invitee_list'] = invitee_list
        context['invitee_list_json'] = False
        context['can_add_invite'] = False
        context['signature_template'] = self.document.flyform.signature_template.render(Context({})) if self.document.is_v1_doc else None

        return context