from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from glynt.apps.document.models import Document, ClientCreatedDocument

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
      msg = ''
      for key, error in form.errors.iteritems():
        if type(key) is int:
            # loop-step
            msg = '<ul class="errorlist"><li>%s</li></ul>' % unicode(_('There were errors in the form. Please see below'))
        else:
            label = form.fields[key].label
            msg += '%s' % (unicode(error).replace('<li>','<li>%s - '%(label,)), )
      status = 400

    return {
        'pk': self.pk if hasattr(self, 'pk') else None,
        'step': self.step,
        'status': status,
        'message': msg,
        'errors': dict(form.errors.items()),
        'object': None,
    }
