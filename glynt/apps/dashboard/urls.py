# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.todo.views import MyToDoListView, ToDoDetailView
from glynt.apps.dashboard.views import CustomerDashboardView


urlpatterns = patterns('',
    url(r'^matching/$', login_required(TemplateView.as_view(template_name="dashboard/matching.html")), name='matching'),
    url(r'^item-test/$', login_required(TemplateView.as_view(template_name="dashboard/item-test.html")), name='matching'),

    url(r'^checklist/(?P<slug>.+)/$', login_required(ToDoDetailView.as_view()), name='item'),
    url(r'^checklist/$', login_required(MyToDoListView.as_view()), name='checklist'),
    url(r'^documents/$', login_required(TemplateView.as_view(template_name='dashboard/documents.html')), name='documents'),
    url(r'^$', login_required(CustomerDashboardView.as_view()), name='overview'),
)
