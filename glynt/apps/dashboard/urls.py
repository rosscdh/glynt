# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.todo.views import ProjectToDoView
from glynt.apps.dashboard.views import DashboardView


urlpatterns = patterns('',
    url(r'^(?P<uuid>.+)/documents/$', login_required(TemplateView.as_view(template_name='dashboard/documents.html')), name='documents'),

    url(r'^(?P<uuid>.+)/checklist/$', login_required(ProjectToDoView.as_view()), name='checklist'),
    url(r'^(?P<uuid>.+)/$', login_required(DashboardView.as_view()), name='project'),
    url(r'^$', login_required(DashboardView.as_view()), name='overview'),
)
