# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='transaction/selection.html'), name='selection'),
    url(r'^intake/$', TemplateView.as_view(template_name='transaction/intake_questionnaire_tmp.html'), name='intake'),
)
