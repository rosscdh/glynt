# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.todo.views import MyToDoListView, ToDoDetailView


urlpatterns = patterns('',
    url(r'^(?P<slug>.+)$', login_required(ToDoDetailView.as_view(), name='todo'),
    url(r'^$', login_required(MyToDoListView.as_view()), name='default'),
)
