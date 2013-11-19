# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from rest_framework import routers

# import the Endpoints & ViewSets
from glynt.apps.customer.api_v2 import (UserViewSet,)

from glynt.apps.project.api_v2 import (ProjectViewSet, DiscussionListView,
                                       TeamListView, DiscussionDetailView,
                                       DiscussionTagView, )
from glynt.apps.todo.api_v2 import (AttachmentViewSet)


# Setup routers
router = routers.DefaultRouter()


# setup Custom urls
urlpatterns = patterns('',
    url(r'^project/(?P<uuid>.+)/team/$',
                                              TeamListView.as_view(),
                                              name='project_team'),
    url(r'^project/(?P<uuid>.+)/discussion/$',
                                              DiscussionListView.as_view(),
                                              name='project_discussion'),
    url(r'^project/(?P<uuid>.+)/todo/(?P<slug>.+)/attachment/$',
                                              AttachmentViewSet.as_view(actions={'get': 'list'}),
                                              name='project_todo_attachment'),
    url(r'^project/(?P<uuid>.+)/discussion/(?P<pk>\d+)/tags((\/(?P<tag>.+))?)/$',
                                              DiscussionTagView.as_view(),
                                              name='project_discussion_tags'),
    url(r'^project/(?P<uuid>.+)/discussion/(?P<pk>\d+)/$',
                                              DiscussionDetailView.as_view(),
                                              name='project_discussion_detail'),
)


# register Viewsets with router
router.register(r'project', ProjectViewSet)
router.register(r'user', UserViewSet)


# Main urlpatterns used by django
urlpatterns += router.urls
