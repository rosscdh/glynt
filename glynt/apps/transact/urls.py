# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='transaction/selection.html'), name='selection'),
    url(r'^second-stage/$', TemplateView.as_view(template_name='transaction/second_stage_tmp.html'), name='second_stage_tmp'),
)
