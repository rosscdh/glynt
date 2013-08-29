# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from glynt.apps.lawyer.forms import LawyerProfileSetupForm
from glynt.apps.lawyer.views import (LawyerListView, LawyerLiteProfileView, 
										LawyerProfileSetupView, LawyerProfileView,)


urlpatterns = patterns('',
    # lawyers
    url(r'^profile/setup/$', login_required(LawyerProfileSetupView.as_view()), name='setup_profile'),
    url(r'^invite/$', login_required(TemplateView.as_view(template_name='lawyer/invite.html')), name='invite'),

    url(r'^welcome/$', login_required(TemplateView.as_view(template_name='lawyer/welcome.html')), name='welcome'),
    url(r'^(?P<slug>.+)/lite/$', LawyerLiteProfileView.as_view(), name='profile_lite'),
    url(r'^(?P<slug>.+)/$', LawyerProfileView.as_view(), name='profile'),
    url(r'^$', LawyerListView.as_view(), name='list'),
)

