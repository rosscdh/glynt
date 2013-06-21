# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import PackagesWizard, FORMS

urlpatterns = patterns('',
    url(r'^$', PackagesWizard.as_view(FORMS)),
)
