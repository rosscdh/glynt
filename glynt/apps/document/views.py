from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, Template
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
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe
from django.db.utils import IntegrityError

from glynt.apps.flyform.forms import BaseFlyForm
from models import Document, DocumentCategory, ClientCreatedDocument

import markdown
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import datetime
import random

from forms import ClientCreatedDocumentForm


FORM_GROUPS = {
  'no_steps': [],
}

def user_can_view_document(document, user):
  """ Helper method for testing a users access to this document """
  
  if type(document) == Document:
    if user.is_superuser or user.is_staff:
      return True
    if document.owner == user and document.doc_status not in [Document.DOC_STATUS.deleted]:
      return True
    if document.is_public == False:
      raise Http404
    if document.doc_status in [Document.DOC_STATUS.deleted, Document.DOC_STATUS.draft]:
      raise Http404

  elif type(document) == ClientCreatedDocument:
    if user.is_superuser or user.is_staff:
      return True
    if document.owner == user:
      return True
    else:
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

    self.document = get_object_or_404(Document.objects.select_related('flyform'), slug=document_slug)

    context['csrf_raw_token'] = get_token(self.request)

    context['object'] = self.document
    context['document'] = self.document.body
    context['default_data'] = json.dumps(self.document.flyform.defaults)
    context['userdoc_form'] = ClientCreatedDocumentForm()

    try:
      context['form_set'] = [BaseFlyForm(json.dumps(step)) for step in self.document.flyform.body]
    except KeyError:
      context['form_set'] = FORM_GROUPS['no_steps']

    user_can_view_document(self.document, self.request.user)

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


class MyDocumentView(DocumentView):
  """ Used when viewing a users own documents """
  def get_context_data(self, **kwargs):
    # call the parent dirctly and skip what the parent would do
    context = super(DocumentView, self).get_context_data(**kwargs)

    document_slug = slugify(self.kwargs['slug'])

    self.user_document = get_object_or_404(ClientCreatedDocument.objects.select_related(), slug=document_slug, owner=self.request.user)
    context['userdoc'] = self.user_document

    context['userdoc_form'] = ClientCreatedDocumentForm(instance=context['userdoc'])

    # Setup the document based on teh source_document of the viewed doc
    self.document = self.user_document.source_document
    context['object'] = self.document
    context['document'] = self.document.body
    context['default_data'] = json.dumps(self.user_document.data)

    try:
      context['form_set'] = [BaseFlyForm(json.dumps(step)) for step in self.document.flyform.body]
    except KeyError:
      context['form_set'] = FORM_GROUPS['no_steps']

    user_can_view_document(self.user_document, self.request.user)

    return context

def userdoc_from_request(user, source_doc=None, pk=None):
  if pk and type(pk) is int:
    userdoc = get_object_or_404(ClientCreatedDocument, pk=pk)
    is_new = False
  else:
    userdoc, is_new = ClientCreatedDocument.objects.get_or_create(owner=user, source_document=source_doc, is_deleted=False)
    # just set the body the first time the object is created
    userdoc.body = source_doc.body
    userdoc.slug = source_doc.slug
  return userdoc, is_new


class DocumentSaveProgressView(View):
  """ Save the user form """
  def post(self, request, *args, **kwargs):
    userdoc_pk = request.POST.get('id', None)
    userdoc_name = request.POST.get('name', None)

    form = ClientCreatedDocumentForm(request.POST)

    if not form.is_valid():
      return HttpResponse('[{"status":"%s", "message":"%s"}]' % (progress.pk, 'error', unicode(_('The form was not valid; please check your data "%s"' %(form.errors,) ))), status=400, content_type="application/json")
    else:
      if not request.user.is_authenticated():
        redirect_url = '%s?next=%s' % (settings.LOGIN_URL, reverse('document:view', kwargs={'slug':document_slug}))
        return HttpResponse('[{"userdoc_id": null, "url": "%s", "status":"%s", "message":"%s"}]' % (redirect_url, 'login_required', unicode(_('Login Required'))), status=200, content_type="application/json")

      document_slug = slugify(self.kwargs['slug'])
      document = get_object_or_404(Document, slug=document_slug)

      progress, is_new = userdoc_from_request(request.user, document, form.cleaned_data['id'])

      progress.name = form.cleaned_data['name']
      progress.data = request.POST.get('current_progress', None)

      saved = False
      slug = base_slug = slugify(form.cleaned_data['name'])
      count = 1
      while saved is not True:
        try:
          progress.slug = slug
          progress.save()
          saved = True
        except IntegrityError:
          slug = '%s-%d' %(base_slug, count,)
          count = count+1
          saved = False

      redirect_url = progress.get_absolute_url()

      return HttpResponse('[{"userdoc_id": %d, "url": "%s", "status":"%s", "message":"%s"}]' % (progress.pk, redirect_url, 'success', unicode(_('Progress Saved'))), status=200, content_type="application/json")


class PersistClientCreatedDocumentProgressView(View):
  """ Persist a clients cookie data as they progress through form """
  def post(self, request, *args, **kwargs):
    userdoc_pk = request.POST.get('id', None)
    userdoc_name = request.POST.get('name', None)

    # is never new
    progress, is_new = userdoc_from_request(user=request.user, source_doc=None, pk=int(self.kwargs['pk']))

    cookie_data = request.COOKIES.get(progress.cookie_name)

    if cookie_data:
      progress.data = cookie_data
      progress.save()

    return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (progress.pk, 'success_persisted', unicode(_('Progress Persisted'))), status=200, content_type="application/json")


class DocumentExportView(View):
    def post(self, request, *args, **kwargs):
      userdoc_pk = request.POST.get('id', None)
      content_markdown = request.POST.get('md', None)

      document_slug = slugify(self.kwargs['slug'])
      document = get_object_or_404(ClientCreatedDocument, slug=document_slug, owner=request.user)

      if content_markdown not in [None,'']:
        html = markdown.markdown(content_markdown)
      else:
        template = Template(document.body)
        html = markdown.markdown(template.render(Context(document.data)))

      result = StringIO.StringIO()
      pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)

      rnd = random.random()
      rnd = '%s' % (str(rnd)[2:6])
      file_name = 'doc_gen/%s-%s-%s.pdf' %(request.user.username, rnd, slugify(document.name),)

      if pdf.err:
        response = HttpResponse('[{"message":"%s"}]'%(pdf.err), status=401, content_type="text/json")
      else:
        pdf_file = default_storage.save(file_name, ContentFile(result.getvalue()))
        response = HttpResponse('[{"filename":"%s%s"}]'%(settings.MEDIA_URL,file_name), status=200, content_type="text/json")

      return response


class CloneClientCreatedDocumentView(View):
  def post(self, request, *args, **kwargs):
    client_document = get_object_or_404(ClientCreatedDocument, pk=self.kwargs['pk'])
    client_document.pk = None # set the pk to null which will cause the ORM to save as a new object
    saved = False
    while saved is not True:
      try:
        client_document.name = 'Copy of %s' % (client_document.name,)
        client_document.slug = slugify(client_document.name)
        client_document.save()
        saved = True
      except IntegrityError:
        saved = False


    url = reverse('document:my_view', kwargs={'slug':client_document.slug})
    message = _("Cloned %s") % (client_document.name,)

    return HttpResponse('[{"userdoc_id": %d, "url":"%s", "status":"%s", "message":"%s"}]' % (client_document.pk, url, 'cloned', unicode(message),), status=200, content_type="application/json")


class DeleteClientCreatedDocumentView(View):
  def post(self, request, *args, **kwargs):
    client_document = get_object_or_404(ClientCreatedDocument, pk=self.kwargs['pk'])
    client_document.is_deleted = True
    client_document.slug = '%d-%s' % (client_document.pk, client_document.slug[0:45],)
    client_document.save()
    message = _("Deleted %s, <a class='undelete-my-document' href='%s'>undo</a>") % (client_document.name, reverse('document:my_undelete', kwargs={'pk':client_document.pk}),)

    return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (client_document.pk, 'deleted', unicode(message),), status=200, content_type="application/json")


class UndoDeleteClientCreatedDocumentView(View):
  def post(self, request, *args, **kwargs):
    client_document = get_object_or_404(ClientCreatedDocument, pk=self.kwargs['pk'])
    if client_document.is_deleted is True:
      client_document.is_deleted = False

      slug = base_slug = client_document.slug.replace('%d-'%(client_document.pk,), '')
      saved = False
      count = 1
      while saved is not True:
        try:
          client_document.slug = slug
          client_document.save()
          saved = True
        except IntegrityError:
          slug = '%s-%d' %(base_slug, count,)
          count = count+1
          saved = False
    message = __("Reactivated '%s'") % (client_document.name,)
    return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (client_document.pk, 'deleted', message,), status=200, content_type="application/json")

