# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from glynt.apps.startup.forms import StartupProfileSetupForm
from glynt.apps.startup.views import StartupListView, StartupProfileSetupView, StartupProfileView


urlpatterns = patterns('',
    # lawyers
    url(r'^profile/setup/$', login_required(template_name='startup/sign-up-form.html'), name='setup_profile'),
    url(r'^invite/$', login_required(TemplateView.as_view(template_name='startup/invite.html')), name='invite'),

    url(r'^$', login_required(TemplateView.as_view(template_name='startup/welcome.html')), name='welcome'),
    # no profile for startups #url(r'^(?P<slug>.+)/$', login_required(LawyerProfileView.as_view()), name='profile'),
    # also no list for startups #url(r'^$', login_required(LawyerListView.as_view()), name='list'),
)
