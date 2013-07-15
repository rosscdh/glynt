# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .forms import DummyBuilderForm

from views import BuilderWizardView, SaveStepView

urlpatterns = patterns('',
    url(r'^build/(?P<tx_range>.+)/(?P<step>.+)/$', login_required(BuilderWizardView.as_view(form_list=[DummyBuilderForm], url_name='transact:builder')), name='builder'),
    url(r'^build/(?P<step>.+)/save/$', login_required(SaveStepView.as_view()), name='save_builder_step'),
)
