# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import StartupEngageLawyerView, EngagementView, CloseEngagementView, ReOpenEngagementView, MyEngagementsView

urlpatterns = patterns('',
    url(r'^lawyer/(?P<lawyer_pk>\d+)/as/startup/$', login_required(StartupEngageLawyerView.as_view()), name='startup_lawyer'),
    url(r'^(?P<slug>.+)/close/$', login_required(CloseEngagementView.as_view()), name='close'),
    url(r'^(?P<slug>.+)/re-open/$', login_required(ReOpenEngagementView.as_view()), name='re-open'),
    url(r'^(?P<slug>.+)/$', login_required(EngagementView.as_view()), name='engagement'),
    url(r'^$', login_required(MyEngagementsView.as_view()), name='list'),
)