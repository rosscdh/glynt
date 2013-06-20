# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from views import StartupProfileSetupView, FounderProfileView, FounderQuestionnaireWizard
from forms import FounderQuestionnaire1, FounderQuestionnaire2

urlpatterns = patterns('',
    url(r'^profile/setup/$', login_required(StartupProfileSetupView.as_view()), name='setup_profile'),
    url(r'^invite/$', login_required(TemplateView.as_view(template_name='startup/invite.html')), name='invite'),

    #url(r'^$', login_required(TemplateView.as_view(template_name='startup/welcome.html')), name='welcome'),
    url(r'^$', login_required(RedirectView.as_view(url=reverse_lazy('lawyer:list'))), name='welcome'),
    url(r'^founder/(?P<slug>.+)/$', login_required(FounderProfileView.as_view()), name='founder_profile'),
    # also no list for startups #url(r'^$', login_required(LawyerListView.as_view()), name='list'),
    url(r'^questionnaire/$', FounderQuestionnaireWizard.as_view([FounderQuestionnaire1, FounderQuestionnaire2]), name='questionnaire')
)