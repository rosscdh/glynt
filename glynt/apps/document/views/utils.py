from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseBadRequest

from glynt.apps.document.models import Document, ClientCreatedDocument

import logging
logger = logging.getLogger(__name__)


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
      for key,field in form.fields.iteritems():
        if key in form.errors:
          label = form.fields[key].label
          msg += '%s' % (str(form.errors[key]).replace('<li>','<li>%s - '%(label,)), )
      status = 400

    return {
        'pk': self.pk if hasattr(self, 'pk') else None,
        'step': self.step,
        'status': status,
        'message': msg,
        'object': None,
    }

