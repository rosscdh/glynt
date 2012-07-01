from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import loader, Context
from django.views.generic.base import View, TemplateView
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView

from models import Document

from forms import AssassinStep1, AssassinStep2
from forms import WillStep1, WillStep2, WillStep3, WillStep4, WillStep5, WillStep6

#from reportlab.pdfgen import canvas

FORM_GROUPS = {
    'legal': [AssassinStep1, AssassinStep2],
    'legal-will': [WillStep1, WillStep2, WillStep3, WillStep4, WillStep5, WillStep6],
}

class DocumentView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['doc'] = kwargs['doc']

        # the context that will render the requested documents inner details
        document_context = Context(context)
        document_template = 'documents/%s.html' %(kwargs['doc'],)
        document_slug = slugify(kwargs['doc'])

        document = Document.objects.get(slug=document_slug)
        context['object'] = document
        #prepared_document = loader.get_template(document_template)#.render(document_context)
        context['document'] = document_template

        context['form_set'] = FORM_GROUPS[document_slug]

        return context


class DocumentExportView(View):
    def post(self, request, *args, **kwargs):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

        # p = canvas.Canvas(response)

        # p.drawString(100, 100, "Hello world.")
        # p.showPage()
        # p.save()

        return response

