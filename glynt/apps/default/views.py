from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import loader, Context
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormMixin
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from models import Document

import markdown
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import datetime

from forms import AssassinStep1, AssassinStep2
from forms import WillStep1, WillStep2, WillStep3, WillStep4, WillStep5, WillStep6, WillStep7

#from reportlab.pdfgen import canvas

FORM_GROUPS = {
    'legal': [AssassinStep1, AssassinStep2],
    'legal-will': [WillStep7, WillStep1, WillStep2, WillStep3, WillStep4, WillStep5, WillStep6],
}

class DocumentView(TemplateView, FormMixin):

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['doc'] = self.kwargs['doc']

        # the context that will render the requested documents inner details
        document_context = Context(context)
        document_template = 'documents/%s.html' %(self.kwargs['doc'],)
        document_slug = slugify(self.kwargs['doc'])

        document = Document.objects.get(slug=document_slug)
        context['object'] = document
        #prepared_document = loader.get_template(document_template)#.render(document_context)
        context['document'] = document_template

        context['form_set'] = FORM_GROUPS[document_slug]

        return context

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        step = int(self.request.GET.get('step', 0))
        if step > 0:
            step = step - 1
        print step
        print self.kwargs['doc']

        return FORM_GROUPS[self.kwargs['doc']][step]

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DocumentExportView(View):
    def post(self, request, *args, **kwargs):
        content_markdown = request.POST.get('md')

        html = markdown.markdown(content_markdown)

        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)

        file_name = 'doc_gen/%ssome_pdf_customized_name.pdf' %(datetime.datetime.utcnow(),)

        if not pdf.err:
            pdf_file = default_storage.save(file_name, ContentFile(result.getvalue()))

        response = HttpResponse('[{"filename":"%s%s"}]'%(settings.MEDIA_URL,file_name), status=200, content_type="text/json")
        return response

