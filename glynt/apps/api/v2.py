# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from rest_framework import routers

# import the Endpoints & ViewSets
from glynt.apps.customer.api_v2 import (UserViewSet,)

from glynt.apps.project.api_v2 import (ProjectViewSet, DiscussionListView,
                                       TeamListView, DiscussionDetailView,
                                       DiscussionTagView, ProjectActivityView,)
from glynt.apps.todo.api_v2 import (AttachmentViewSet, ToDoActivityView,
                                    ToDoDiscussionDetailView,
                                    ToDoFeedbackRequestView)


# Setup routers
router = routers.DefaultRouter()


# setup Custom urls
project_urlpatterns = patterns('',
    url(r'^project/(?P<uuid>.+)/activity/$',
                                              ProjectActivityView.as_view(),
                                              name='project_activity'),

    url(r'^project/(?P<uuid>.+)/team/$',
                                              TeamListView.as_view(),
                                              name='project_team'),
)

project_todo_urlpatterns = patterns('',
    url(r'^project/(?P<uuid>.+)/todo/(?P<slug>.+)/activity/$',
                                              ToDoActivityView.as_view(actions={'get': 'list'}),
                                              name='project_todo_activity'),
    url(r'^project/(?P<uuid>.+)/todo/(?P<slug>.+)/attachment/$',
                                              AttachmentViewSet.as_view(actions={'get': 'list'}),
                                              name='project_todo_attachment'),
    url(r'^project/(?P<uuid>.+)/todo/(?P<slug>.+)/discussion/((\/(?P<parent_pk>\d+))?)$',
                                              ToDoDiscussionDetailView.as_view(actions={'get': 'list', 'post': 'create', 'patch': 'update'}),
                                              name='project_todo_discussion'),
    url(r'^project/(?P<uuid>.+)/todo/(?P<slug>.+)/feedback_request((\/(?P<pk>\d+))?)/$',
                                              ToDoFeedbackRequestView.as_view(actions={'get': 'list', 'post': 'create', 'patch': 'update', 'delete': 'destroy'}),
                                              name='project_todo_feedbackrequest'),
)

project_discussion_urlpatterns = patterns('',

    url(r'^project/(?P<uuid>.+)/discussion/$',
                                              DiscussionListView.as_view(),
                                              name='project_discussion'),

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


urlpatterns = project_todo_urlpatterns + project_discussion_urlpatterns + project_urlpatterns

# Main urlpatterns used by django
urlpatterns += router.urls
