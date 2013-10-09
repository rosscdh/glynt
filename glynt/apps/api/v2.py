# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from rest_framework import routers

# import the Endpoints & ViewSets
from glynt.apps.project.api_v2 import (ProjectViewSet, DiscussionListView, DiscussionDetailView, )


# Setup routers
router = routers.DefaultRouter()


# setup Custom urls
urlpatterns = patterns('',
    url(r'^project/(?P<uuid>.+)/discussion/$',
                                              DiscussionListView.as_view(),
                                              name='project_discussion_list'),
    url(r'^project/(?P<uuid>.+)/discussion/(?P<pk>.+)/$',
                                              DiscussionDetailView.as_view(),
                                              name='project_discussion_detail'),
)


# register Viewsets with router
router.register(r'project', ProjectViewSet)


# Main urlpatterns used by django
urlpatterns += router.urls
