from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from glynt.apps.smoothe.views import CreateTemplateView, UpdateTemplateView, \
                                     CreateDocumentView, UpdateDocumentView


urlpatterns = patterns('',
    url(r'^template/create/$', login_required(CreateTemplateView.as_view()), name='create_template'),
    url(r'^template/(?P<pk>.+)/edit/$', login_required(UpdateTemplateView.as_view()), name='update_template'),

    # New User Docs are based on Templates
    url(r'^(?P<slug>.*)/create/$', CreateDocumentView.as_view(), name='create_document'), # no login required, to allow user commiteent and signup
    # Editing ClientCreatedDocuments here
    url(r'^my/(?P<pk>.+)/edit/$', login_required(UpdateDocumentView.as_view()), name='update_document'),
)
