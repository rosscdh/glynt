# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import (ToDoDetailView, ToDoDiscussionView, ToDoEditView,\
                    ToDoCreateView, AttachmentView, AttachmentRedirectView,)


urlpatterns = patterns('',
    url(r'^attachment/(?P<pk>\d+)/$', login_required(AttachmentView.as_view()), name='attachment'),
    url(r'^attachment/(?P<pk>\d+)/crocdoc/$', login_required(AttachmentRedirectView.as_view()), name='crocdoc_302'),
    url(r'^(?P<project_uuid>.+)/create/$', login_required(ToDoCreateView.as_view()), name='create'),
    url(r'^(?P<project_uuid>.+)/(?P<slug>.+)/discussion/$', login_required(ToDoDiscussionView.as_view()), name='discuss'),    
    url(r'^(?P<project_uuid>.+)/(?P<slug>.+)/edit/$', login_required(ToDoEditView.as_view()), name='edit'),
    url(r'^(?P<project_uuid>.+)/(?P<slug>.+)/$', login_required(ToDoDetailView.as_view()), name='item'),
)
