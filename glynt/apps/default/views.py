from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

from django.template import loader, Context
from django.views.generic.base import TemplateView


class DocumentView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['doc'] = kwargs['doc']

        # the context that will render the requested documents inner details
        document_context = Context(context)
        document_template = 'documents/%s.html' %(kwargs['doc'],)
        #prepared_document = loader.get_template(document_template)#.render(document_context)

        context['document'] = document_template


        return context

