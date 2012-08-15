from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from views import DocumentView, MyDocumentView, CreateDocumentView, EditDocumentView, DocumentSaveProgressView, DocumentExportView
from views import DocumentByCategoryListView

from glynt.apps.flyform.forms import TmpStepCreator


urlpatterns = patterns('',
    url(r'^category/(?P<type>.+)/(?P<category>.+)/$', DocumentByCategoryListView.as_view(), name='category_list'),

    url(r'^tmp/step/creator/$', login_required(FormView.as_view(form_class=TmpStepCreator, template_name='document/tmp_step_creator.html')), name='step_creator'),
    url(r'^create/$', login_required(CreateDocumentView.as_view()), name='create'),
    url(r'^(?P<slug>.+)/edit/$', login_required(EditDocumentView.as_view()), name='edit'),
    url(r'^(?P<slug>.+)/export/$', login_required(DocumentExportView.as_view()), name='export'),
    # is not login_required as we want users to be redirected to login
    url(r'^(?P<slug>.+)/save/$', DocumentSaveProgressView.as_view(), name='save_progress'),
    url(r'^my/(?P<slug>.+)/$', MyDocumentView.as_view(template_name='document/document.html'), name='my_view'),
    url(r'^(?P<slug>.+)/$', DocumentView.as_view(template_name='document/preview-document.html'), name='view'),
)
