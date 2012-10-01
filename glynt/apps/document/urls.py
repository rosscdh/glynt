from django.conf.urls import patterns, url
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required

from glynt.apps.document.views import DocumentView, MyDocumentView, CreateDocumentView, EditDocumentView, DocumentByCategoryListView
from glynt.apps.document.views import DocumentExportView, CloneClientCreatedDocumentView, DeleteClientCreatedDocumentView, UndoDeleteClientCreatedDocumentView
from glynt.apps.document.views import ValidateClientCreatedDocumentFormView, PersistClientCreatedDocumentProgressView 

from glynt.apps.flyform.forms import TmpStepCreator


urlpatterns = patterns('',
    url(r'^category/(?P<type>.+)/(?P<category>.+)/$', DocumentByCategoryListView.as_view(), name='category_list'),

    # Client Created Documents
    url(r'^my/(?P<pk>\d+)/delete/$', login_required(DeleteClientCreatedDocumentView.as_view()), name='my_delete'),
    url(r'^my/(?P<pk>\d+)/undelete/$', login_required(UndoDeleteClientCreatedDocumentView.as_view()), name='my_undelete'),
    url(r'^my/(?P<pk>\d+)/clone/$', login_required(CloneClientCreatedDocumentView.as_view()), name='my_clone'),
    url(r'^my/(?P<pk>\d+)/persist/$', login_required(PersistClientCreatedDocumentProgressView.as_view()), name='my_persist'),
    url(r'^my/(?P<slug>.+)/$', login_required(MyDocumentView.as_view(template_name='document/document.html')), name='my_view'),

    url(r'^tmp/step/creator/$', login_required(FormView.as_view(form_class=TmpStepCreator, template_name='document/tmp_step_creator.html')), name='step_creator'),
    url(r'^create/$', login_required(CreateDocumentView.as_view()), name='create'),
    url(r'^(?P<slug>.+)/edit/$', login_required(EditDocumentView.as_view()), name='edit'),
    url(r'^(?P<slug>.+)/export/$', login_required(DocumentExportView.as_view()), name='export'),
    # is not login_required as we want users to be redirected to login
    url(r'^(?P<slug>.+)/save/$', ValidateClientCreatedDocumentFormView.as_view(), name='validate_form'),
    url(r'^(?P<slug>.+)/$', DocumentView.as_view(template_name='document/preview-document.html'), name='view'),
)
