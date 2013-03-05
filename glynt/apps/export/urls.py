from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from glynt.apps.export.views import ExportAsPDFView, ExportAsHTMLView


urlpatterns = patterns('',
    # Export
    url(r'^(?P<pk>\d+)/pdf/$', login_required(ExportAsPDFView.as_view()), name='as_pdf'),
    url(r'^(?P<pk>\d+)/html/$', login_required(ExportAsHTMLView.as_view()), name='as_html'),
)
