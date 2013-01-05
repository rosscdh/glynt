from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.smoothe.views import MyDocumentView, CreateDocumentView, UpdateDocumentView


urlpatterns = patterns('',
    url(r'^create/$', login_required(CreateDocumentView.as_view()), name='create'),
    url(r'^(?P<pk>\d+)/edit/$', login_required(UpdateDocumentView.as_view()), name='update'),
    url(r'^my/(?P<slug>.+)/$', login_required(MyDocumentView.as_view()), name='view'),
)
