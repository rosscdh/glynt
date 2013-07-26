# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.todo.views import ProjectToDoView
from glynt.apps.dashboard.views import CustomerDashboardView


urlpatterns = patterns('',
    url(r'^checklist/open/$', login_required(TemplateView.as_view(template_name='todo/item_DELETE/open.html')), name='item-open'),
    url(r'^checklist/pending/$', login_required(TemplateView.as_view(template_name='todo/item_DELETE/pending.html')), name='item-pending'),
    url(r'^checklist/resolved/$', login_required(TemplateView.as_view(template_name='todo/item_DELETE/resolved.html')), name='item-resolved'),
    url(r'^checklist/discussion/$', login_required(TemplateView.as_view(template_name='todo/item_DELETE/discussion.html')), name='item-discussion'),


    url(r'^(?P<uuid>.+)/documents/$', login_required(TemplateView.as_view(template_name='dashboard/documents.html')), name='documents'),
    # url(r'^(?P<uuid>.+)/checklist/(?P<item_status>.+)/$', login_required(ProjectToDoView.as_view()), name='checklist_by_status'),
    url(r'^(?P<uuid>.+)/checklist/$', login_required(ProjectToDoView.as_view()), name='checklist'),
    url(r'^(?P<uuid>.+)/$', login_required(CustomerDashboardView.as_view()), name='project'),
    url(r'^$', login_required(CustomerDashboardView.as_view()), name='overview'),


    url(r'^matching/$', login_required(TemplateView.as_view(template_name="dashboard/matching.html")), name='matching'),
    url(r'^matched/$', login_required(TemplateView.as_view(template_name="dashboard/matched.html")), name='matched'),


    # url(r'^checklist/(?P<slug>.+)/$', login_required(ToDoDetailView.as_view()), name='item'),
)
