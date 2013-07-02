# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import CompanyEngageLawyerView, ProjectView, CloseProjectView, ReOpenProjectView, MyProjectsView

urlpatterns = patterns('',
    url(r'^lawyer/(?P<lawyer_pk>\d+)/as/startup/$', login_required(CompanyEngageLawyerView.as_view()), name='startup_lawyer'),
    url(r'^(?P<slug>.+)/close/$', login_required(CloseProjectView.as_view()), name='close'),
    url(r'^(?P<slug>.+)/re-open/$', login_required(ReOpenProjectView.as_view()), name='re-open'),
    url(r'^(?P<slug>.+)/$', login_required(ProjectView.as_view()), name='project'),
    url(r'^$', login_required(MyProjectsView.as_view()), name='list'),
)