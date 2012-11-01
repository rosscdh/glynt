from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.export.views import ExportAsPDFView


urlpatterns = patterns('',
    # Export
    url(r'^(?P<slug>.+)/pdf/$', login_required(ExportAsPDFView.as_view()), name='as_pdf'),
)
