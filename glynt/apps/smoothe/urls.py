from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.smoothe.views import MyDocumentView


urlpatterns = patterns('',
    url(r'^my/(?P<slug>.+)/$', login_required(MyDocumentView.as_view()), name='view'),
)
