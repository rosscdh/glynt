# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import (ToDoDetailView, ToDoCommentView, ToDoEditView, ToDoAttachmentView, ToDoAssignView,)


urlpatterns = patterns('',
    url(r'^(?P<project_uuid>.+)/(?P<slug>.+)/discussion/$', login_required(ToDoCommentView.as_view()), name='discussion'),
    url(r'^(?P<project_uuid>.+)/(?P<slug>.+)/edit/$', login_required(ToDoEditView.as_view()), name='edit'),
    url(r'^(?P<project_uuid>.+)/(?P<slug>.+)/attachment/$', login_required(ToDoAttachmentView.as_view()), name='attachment'),
    url(r'^(?P<project_uuid>.+)/(?P<slug>.+)/assign/$', login_required(ToDoAssignView.as_view()), name='assign'),
    url(r'^(?P<project_uuid>.+)/(?P<slug>.+)$', login_required(ToDoDetailView.as_view()), name='todo'),
    #url(r'^$', login_required(MyToDoListView.as_view()), name='default'),
)
