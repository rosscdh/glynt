# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .forms import DummyBuilderForm

from views import BuilderWizardView

urlpatterns = patterns('',
    url(r'^build/(?P<tx_range>.+)/$', login_required(BuilderWizardView.as_view(form_list=[DummyBuilderForm])), name='builder'),
)
