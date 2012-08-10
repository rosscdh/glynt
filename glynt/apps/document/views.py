from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, Context
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from django.utils import simplejson as json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.shortcuts import get_object_or_404

from glynt.apps.flyform.forms import BaseFlyForm
from models import Document, DocumentCategory, ClientCreatedDocument

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


class DocumentByCategoryListView(ListView):
    model = Document
    template_name = 'document/documentcategory_list.html'

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an interable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        self.doc_type = self.kwargs.get('type', None)
        self.category = self.kwargs.get('category', None)

        queryset = self.model.objects.filter(doc_cats__slug=self.category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(DocumentByCategoryListView, self).get_context_data(**kwargs)

        context['category'] = DocumentCategory.objects.get(slug=self.category)
        context['doc_type'] = self.doc_type

        return context


class CreateDocumentView(TemplateView, FormMixin):
    template_name = 'document/create.html'


class EditDocumentView(TemplateView, FormMixin):
    template_name = 'document/create.html'


class DocumentView(TemplateView, FormMixin, JsonErrorResponseMixin):

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)

        document_slug = slugify(self.kwargs['slug'])
        self.document = Document.objects.get(slug=document_slug)
        context['object'] = self.document
        context['document'] = self.document.body

        try:
            context['form_set'] = [BaseFlyForm(json.dumps(s)) for s in self.document.flyform.body]
        except KeyError:
            context['form_set'] = FORM_GROUPS['no_steps']

        user_can_view_document(context, self.request.user)

        return context

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return BaseFlyForm

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()

        self.step = int(self.request.GET.get('step', 0))
        if self.step > 0:
            self.step = self.step - 1

        kwargs['json_form'] = self.document.flyform.body[self.step]

        return form_class(**kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        response = self.get_response_json(form)

        return HttpResponse(json.dumps(response), status=response['status'], content_type='text/json')


class DocumentSaveProgressView(View):
  def post(self, request, *args, **kwargs):

    document_slug = slugify(self.kwargs['slug'])
    document = get_object_or_404(Document, slug=document_slug)
    progress, is_new = ClientCreatedDocument.objects.get_or_create(owner=request.user, source_document=document)
    progress.body = request.POST.get('md', None)
    progress.data = request.POST.get('current_progress', None)
    progress.save()

    response = HttpResponse('[{"status":"%s", "message":"%s"}]' % ('success', unicode(_('Progress Saved'))), status=200, content_type="text/json")
    return response


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

