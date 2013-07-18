# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .forms import DummyBuilderForm

from views import BuilderWizardView

urlpatterns = patterns('',
    url(r'^build/(?P<project_uuid>.+)/(?P<tx_range>.+)/(?P<step>.+)/$', login_required(BuilderWizardView.as_view(form_list=[DummyBuilderForm], url_name='transact:builder')), name='builder'),
)
