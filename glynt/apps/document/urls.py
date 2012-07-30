from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from views import DocumentView, CreateDocumentView, EditDocumentView, DocumentExportView

urlpatterns = patterns('',
	url(r'^create/$', login_required(CreateDocumentView.as_view()), name='create'),
	url(r'^(?P<slug>.+)/edit/$', login_required(EditDocumentView.as_view()), name='edit'),
    url(r'^(?P<slug>.+)/export/$', login_required(DocumentExportView.as_view()), name='export'),
    url(r'^(?P<slug>.+)/$', DocumentView.as_view(template_name='document/document.html'), name='view'),
)
