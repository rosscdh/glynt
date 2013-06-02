# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from glynt.apps.graph.views import me, connections_for_user, user_to_user

urlpatterns = patterns('',
    # Graph Views
    url(r'^me/$', login_required(me)),
    url(r'^(?P<pk>\d+)/$', login_required(connections_for_user)),
    url(r'^common/(?P<pk>\d+)/(?P<pk>\d+)/$', login_required(user_to_user)),
)
