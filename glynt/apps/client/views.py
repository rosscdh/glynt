from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect

from glynt.apps.document.models import Document


class DashboardView(TemplateView):
    template_name = 'client/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['document_list'] = Document.objects.filter(owner=self.request.user)

        return context
