# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .forms import DummyBuilderForm

from views import BuilderWizardView
from views import IntakeWizard, INTAKE_FORMS

urlpatterns = patterns('',
    url(r'^intake/$', login_required(IntakeWizard.as_view(INTAKE_FORMS)), name='intake'),
    url(r'^build/(?P<tx_range>.+)/$', login_required(BuilderWizardView.as_view(form_list=[DummyBuilderForm])), name='builder'),
)
