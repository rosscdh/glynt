from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from views import DocumentView, CreateDocumentView, DocumentExportView


urlpatterns = patterns('',
    url(r'^(?P<slug>.+)/export/$', DocumentExportView.as_view(), name='export'),
    url(r'^create/$', CreateDocumentView.as_view(), name='create'),
    url(r'^(?P<slug>.+)/$', DocumentView.as_view(template_name='document/document.html'), name='view'),
)
