# -*- coding: utf-8 -*-
from django import forms
from django.template.defaultfilters import slugify
from bootstrap.forms import BootstrapModelForm, Fieldset

from glynt.apps.document.models import DocumentTemplate
from glynt.apps.document.models import ClientCreatedDocument

import logging
logger = logging.getLogger(__file__)


class DocumentTemplateForm(BootstrapModelForm):
    class Meta:
        model = DocumentTemplate
        exclude = ('slug',)
        layout = (
            Fieldset('Document Authoring', 'body'),
            Fieldset('Document Properties', 'name', 'owner', 'acronym', 'summary', 'description', 'doc_status', 'is_public', 'doc_category'),
        )

    def save(self, commit=True):
        if self.instance.pk is None:
            # New
            if not self.instance.slug:
                self.instance.slug = slugify(self.instance.name)

        return super(DocumentTemplateForm, self).save(commit=commit)


#@TODO: add tests for this form
class ClientDocumentForm(forms.ModelForm):
    class Meta:
        model = ClientCreatedDocument

    def __init__(self, *args, **kwargs):
        """ Handle accessing the request object form this form"""
        self.request = kwargs.pop('request') if 'request' in kwargs else None
        self.source_document = kwargs.pop('source_document') if 'source_document' in kwargs else None

        if 'data' in kwargs:
            doc_data = kwargs['data']
            kwargs['data'] = kwargs['data'].copy() # make it mutable

            if kwargs['instance'] is not None:
                source = kwargs['instance']
                kwargs['data']['doc_data'] = doc_data

                kwargs['data'].setdefault('doc_data', doc_data) # ensure the primary json is saved
                kwargs['data'].setdefault('owner', source.owner.pk)
                kwargs['data'].setdefault('source_document', source.source_document.pk)
                kwargs['data'].setdefault('name', source.name)
                kwargs['data'].setdefault('slug', source.slug)
                kwargs['data'].setdefault('meta_data', source.meta_data)
                kwargs['data'].setdefault('body', source.body)

            else:
                kwargs['data'].setdefault('doc_data', doc_data) # ensure the primary json is saved
                kwargs['data'].setdefault('owner', self.request.user.pk)
                kwargs['data'].setdefault('source_document', self.source_document.pk)
                kwargs['data'].setdefault('name', self.source_document.name)
                kwargs['data'].setdefault('slug', '%s-%s' % (self.source_document.pk, self.request.user.pk,))
                kwargs['data'].setdefault('meta_data', {})
                kwargs['data'].setdefault('body', self.source_document.body)

        super(ClientDocumentForm, self).__init__(*args, **kwargs)

    def clean_slug(self):
        """ @TODO move to utils and make mixin """
        slug = self.cleaned_data.get('slug')
        # slug is there and this is a new instance
        if slug and self.instance.pk is None:
            original_slug = slug
            avail = False
            counter = 1
            while not avail and counter < 15:
                try:
                    item = self.Meta.model.objects.get(slug=slug)
                    counter += 1
                    slug = '%s-%d' %(original_slug, counter,)
                except self.Meta.model.DoesNotExist:
                    avail = True

        return slug
