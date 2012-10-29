from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.document.views import AuthorToolView, DocumentView, MyDocumentView, DocumentByCategoryListView
from glynt.apps.document.views import CloneClientCreatedDocumentView, DeleteClientCreatedDocumentView, UndoDeleteClientCreatedDocumentView
from glynt.apps.document.views import ReviewClientCreatedView, ValidateClientCreatedDocumentFormView, PersistClientCreatedDocumentProgressView 


urlpatterns = patterns('',
    url(r'^category/(?P<type>.+)/(?P<category>.+)/$', DocumentByCategoryListView.as_view(), name='category_list'),

    # Client Created Documents
    url(r'^my/(?P<pk>\d+)/delete/$', login_required(DeleteClientCreatedDocumentView.as_view()), name='my_delete'),
    url(r'^my/(?P<pk>\d+)/undelete/$', login_required(UndoDeleteClientCreatedDocumentView.as_view()), name='my_undelete'),
    url(r'^my/(?P<pk>\d+)/clone/$', login_required(CloneClientCreatedDocumentView.as_view()), name='my_clone'),
    url(r'^my/(?P<pk>\d+)/persist/$', login_required(PersistClientCreatedDocumentProgressView.as_view()), name='my_persist'),
    url(r'^my/(?P<slug>.+)/review/$', login_required(ReviewClientCreatedView.as_view()), name='my_review'),
    url(r'^my/(?P<slug>.+)/$', login_required(MyDocumentView.as_view(template_name='document/document.html')), name='my_view'),

    # Authoring
    url(r'^author/$', login_required(AuthorToolView.as_view()), name='author_doc'),
    url(r'^(?P<pk>\d+)/author/$', login_required(AuthorToolView.as_view()), name='author_edit_doc'),

    # is not login_required as we want users to be redirected to login
    url(r'^(?P<slug>.+)/save/$', login_required(ValidateClientCreatedDocumentFormView.as_view()), name='validate_form'),
    url(r'^(?P<slug>.+)/$', DocumentView.as_view(template_name='document/preview-document.html'), name='view'),
)
