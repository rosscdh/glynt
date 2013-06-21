# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import PackagesWizard, FORMS

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='transaction/selection.html'), name='selection'),
    url(r'^packages/$', PackagesWizard.as_view(FORMS)),
)
