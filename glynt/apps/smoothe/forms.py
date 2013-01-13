# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from bootstrap.forms import BootstrapModelForm, Fieldset

from glynt.apps.document.models import DocumentTemplate
from glynt.apps.document.models import ClientCreatedDocument


class DocumentTemplateForm(BootstrapModelForm):
    class Meta:
        model = DocumentTemplate
        exclude = ('slug',)
        layout = (
            Fieldset('Document Authoring', 'body'),
            Fieldset('Document Properties', 'name', 'owner', 'acronym', 'summary', 'description', 'doc_status', 'is_public', 'doc_cats'),
        )

    def save(self, commit=True):
        if self.instance.pk is None:
            # New
            if not self.instance.slug:
                self.instance.slug = slugify(self.instance.name)

        return super(DocumentTemplateForm, self).save(commit=commit)


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
