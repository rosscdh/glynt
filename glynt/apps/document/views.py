from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, Context
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormMixin
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from django.utils import simplejson as json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from models import Document

import markdown
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import datetime

from forms import AssassinStep1, AssassinStep2
from forms import WillStep1, WillStep2, WillStep3, WillStep4, WillStep5, WillStep6, WillStep7
#from reportlab.pdfgen import canvas

FORM_GROUPS = {
    'no_steps': [],
    'legal': [AssassinStep1, AssassinStep2],
    'legal-will': [WillStep1, WillStep2, WillStep3, WillStep4, WillStep5, WillStep6, WillStep7]
}

def user_can_view_document(context, user):
    """ Helper method for testing a users access to this document """
    document = context['object']
    if user.is_superuser or user.is_staff:
        return True
    if document.owner == user and document.doc_status not in [Document.DOC_STATUS.deleted]:
        return True
    if document.is_public == False:
        raise Http404
    if document.doc_status in [Document.DOC_STATUS.deleted, Document.DOC_STATUS.draft]:
        raise Http404


class JsonErrorResponseMixin(object):
    def get_response_json(self, form):
        if form.is_valid():
            msg = None
            status = 200
        else:
            msg = str(form.errors)
            status = 400

        return {
            'pk': self.pk if hasattr(self, 'pk') else None,
            'step': self.step,
            'status': status,
            'message': msg,
            'object': None,
        }

class CreateDocumentView(TemplateView, FormMixin):
    template_name = 'document/create.html'


class EditDocumentView(TemplateView, FormMixin):
    template_name = 'document/create.html'


class DocumentView(TemplateView, FormMixin, JsonErrorResponseMixin):

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)

        document_slug = slugify(self.kwargs['slug'])
        document = Document.objects.get(slug=document_slug)
        context['object'] = document
        context['document'] = document.body

        try:
            context['form_set'] = FORM_GROUPS[document_slug]
        except KeyError:
            context['form_set'] = FORM_GROUPS['no_steps']

        user_can_view_document(context, self.request.user)

        return context

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        self.step = int(self.request.GET.get('step', 0))
        if self.step > 0:
            self.step = self.step - 1

        return FORM_GROUPS[self.kwargs['doc']][self.step]

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        response = self.get_response_json(form)

        return HttpResponse(json.dumps(response), status=response['status'], content_type='text/json')


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

