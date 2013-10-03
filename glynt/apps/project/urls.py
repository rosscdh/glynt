# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import (ProjectView, CreateProjectView, CloseProjectView, 
                    ReOpenProjectView,
                    ProjectCategoryView,
                    LawyerContactProjectView,)

urlpatterns = patterns('',
    url(r'^create/$', login_required(CreateProjectView.as_view()), name='create'),

    url(r'^(?P<slug>.+)/(?P<lawyer>.+)/project-contact/$', login_required(LawyerContactProjectView.as_view()), name='project_contact'),

    url(r'^(?P<slug>.+)/category/$', login_required(ProjectCategoryView.as_view()), name='category'),

    url(r'^(?P<slug>.+)/close/$', login_required(CloseProjectView.as_view()), name='close'),
    url(r'^(?P<slug>.+)/re-open/$', login_required(ReOpenProjectView.as_view()), name='re-open'),
    url(r'^(?P<slug>.+)/$', login_required(ProjectView.as_view()), name='project'),
)
