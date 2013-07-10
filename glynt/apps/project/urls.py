# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

# from glynt.apps.transact.views import PackagesWizard, FORMS
from views import ProjectView, CreateProjectView, CloseProjectView, ReOpenProjectView, MyProjectsView

urlpatterns = patterns('',
    # url(r'^create/$', login_required(PackagesWizard.as_view(FORMS)), name='create'),
    url(r'^my/$', login_required(MyProjectsView.as_view()), name='list'),
    url(r'^(?P<slug>.+)/close/$', login_required(CloseProjectView.as_view()), name='close'),
    url(r'^(?P<slug>.+)/re-open/$', login_required(ReOpenProjectView.as_view()), name='re-open'),
    url(r'^(?P<slug>.+)/$', login_required(ProjectView.as_view()), name='project'),
)
