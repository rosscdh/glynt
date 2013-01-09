from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.smoothe.views import CreateDocumentView, UpdateDocumentView, \
                                     CreateTemplateView, CreateTemplateView as UpdateTemplateView


urlpatterns = patterns('',
    url(r'^template/create/$', login_required(CreateTemplateView.as_view()), name='create_template'),
    url(r'^template/(?P<slug>.+)/edit/$', login_required(UpdateTemplateView.as_view()), name='update_template'),

    # New User Docs are based on Templates
    url(r'^my/create/(?P<slug>.+)/$', login_required(CreateDocumentView.as_view()), name='create_document'),
    url(r'^my/(?P<pk>.+)/edit/$', login_required(UpdateDocumentView.as_view()), name='update_document'),
)
