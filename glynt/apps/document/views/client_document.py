# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseBadRequest
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
from django.views.generic.base import View, TemplateView
from django.utils import simplejson as json
from django.db.utils import IntegrityError, DatabaseError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from glynt.apps.document.models import Document, ClientCreatedDocument
from glynt.apps.document.forms import ClientCreatedDocumentForm

from glynt.apps.flyform.forms import BaseFlyForm

from document import DocumentView
from utils import user_can_view_document

import markdown
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import random

import logging
logger = logging.getLogger(__name__)

FORM_GROUPS = {
  'no_steps': [],
}


def userdoc_from_request(user, source_doc=None, pk=None):
  if pk and type(pk) is int:
    logger.debug('got pk so can get ClientCreatedDocument directly')
    userdoc = get_object_or_404(ClientCreatedDocument, pk=pk)
    is_new = False
  else:
    userdoc = ClientCreatedDocument.objects.create(owner=user, source_document=source_doc, is_deleted=False)
    is_new = True
    logger.debug('got no pk so must get ClientCreatedDocument based on user source_document and is_deleted=False: document:%s is_new:%s'%(userdoc, is_new,))
    # just set the body the first time the object is created
    userdoc.body = source_doc.body
    userdoc.slug = source_doc.slug
  return userdoc, is_new


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
      context['form_set'] = [BaseFlyForm(step_num, json.dumps(step)) for step_num, step in enumerate(self.document.flyform.body)]
    except KeyError:
      context['form_set'] = FORM_GROUPS['no_steps']

    user_can_view_document(self.user_document, self.request.user)

    return context


# @TODO rename to ClientCreatedClientCreatedDocumentSaveProgressView
class ClientCreatedDocumentSaveProgressView(View):
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
    userdoc_current_progress = request.POST.get('current_progress', None)
    userdoc_pk = int(self.kwargs['pk'])

    # is never new
    progress, is_new = userdoc_from_request(user=request.user, source_doc=None, pk=userdoc_pk)

    if userdoc_current_progress:
      progress.data = userdoc_current_progress
      progress.save()

    return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (progress.pk, 'success_persisted', unicode(_('Progress Persisted'))), status=200, content_type="application/json")


# @TODO rename to ClientCreatedDocumentExportView
class DocumentExportView(View):
    def post(self, request, *args, **kwargs):
      userdoc_pk = request.POST.get('id', None)
      content_markdown = request.POST.get('md', None)

      document_slug = slugify(self.kwargs['slug'])
      document = get_object_or_404(ClientCreatedDocument.objects.select_related('source_document','source_document__flyform'), slug=document_slug, owner=request.user)
      logger.debug('got document: %s'%(document,))

      if content_markdown not in [None,'']:
        html = markdown.markdown(content_markdown)
        logger.debug('markdown was provided: %s'%(content_markdown,))
      else:
        logger.debug('no markdown was provided generate based on default_data and pybars')
        if type(document.source_document.flyform.defaults) is dict:
          data = dict(document.source_document.flyform.defaults.items() + document.data.items())
          logger.debug('flyform.defaults was combined with document.body')
        else:
          data = document.data
          logger.debug('flyform.defaults was not specified')

        t = Template(document.body)
        c = Context(data)
        html = t.render(c)
        # html = markdown.markdown(template.render(Context(document.data)))
        print html

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
      except IntegrityError, DatabaseError:
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
    message = _("Deleted %s, <a id='undelete-%d' class='undelete-my-document' href='%s'>undo</a>") % (client_document.name, client_document.pk, reverse('document:my_undelete', kwargs={'pk':client_document.pk}),)

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
    message = _("Reactivated '%s'") % (client_document.name,)
    return HttpResponse('[{"userdoc_id": %d, "status":"%s", "message":"%s"}]' % (client_document.pk, 'deleted', message,), status=200, content_type="application/json")

