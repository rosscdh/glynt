# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from bootstrap.forms import BootstrapModelForm, Fieldset

from glynt.apps.document.models import Document
from glynt.apps.document.models import ClientCreatedDocument


class DocumentForm(BootstrapModelForm):
    class Meta:
        model = Document
        layout = (
            Fieldset('Document Authoring', 'body'),
            Fieldset('Document Properties', 'name', 'slug', 'owner', 'summary', 'doc_status', 'is_public', 'doc_cats', 'tags'),
        )


class ClientDocumentForm(forms.ModelForm):
    class Meta:
        model = ClientCreatedDocument

    def __init__(self, *args, **kwargs):
        """ Handle accessing the request object form this form"""
        self.request = kwargs.pop('request')
        self.source_document = kwargs.pop('source_document')

        if 'data' in kwargs:
            kwargs['data'] = kwargs['data'].copy() # make it mutable
            kwargs['data'].setdefault('owner', self.request.user.pk)
            kwargs['data'].setdefault('source_document', self.source_document.pk)
            kwargs['data'].setdefault('name', self.source_document.name)
            kwargs['data'].setdefault('slug', '%s-%s' % (self.request.user.pk, self.source_document.pk,))
            kwargs['data'].setdefault('data', {})
            kwargs['data'].setdefault('meta_data', {})
            kwargs['data'].setdefault('body', 'blank')

        super(ClientDocumentForm, self).__init__(*args, **kwargs)

