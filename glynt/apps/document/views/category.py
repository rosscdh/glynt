from django.views.generic.list import ListView

from glynt.apps.document.models import DocumentTemplate, DocumentTemplateCategory

import logging
logger = logging.getLogger(__name__)


class DocumentByCategoryListView(ListView):
  model = DocumentTemplate
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

    context['category'] = DocumentTemplateCategory.objects.get(slug=self.category)
    context['doc_type'] = self.doc_type

    return context