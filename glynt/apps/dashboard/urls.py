# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.todo.views import MyToDoListView, ToDoDetailView


urlpatterns = patterns('',
    url(r'^checklist/(?P<id>[a-zA-Z0-9]{24})$', login_required(ToDoDetailView.as_view()), name='item'),
    url(r'^checklist$', login_required(MyToDoListView.as_view()), name='checklist'),
    url(r'^documents$', login_required(TemplateView.as_view(template_name='dashboard/documents.html')), name='documents'),
    url(r'^$', login_required(TemplateView.as_view(template_name='dashboard/overview.html')), name='overview'),
)
