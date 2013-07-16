# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import ConfirmLoginDetailsView, DashboardView
from glynt.decorators import anonymous_required


urlpatterns = patterns('',
    url(r'^signup/(?P<slug>.+)/confirm/$', login_required(ConfirmLoginDetailsView.as_view()), name='confirm_signup'),
    url(r'^$', login_required(DashboardView.as_view()), name='dashboard'),
)
