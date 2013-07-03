# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from views import CompanyProfileSetupView


urlpatterns = patterns('',
    url(r'^profile/setup/$', login_required(CompanyProfileSetupView.as_view()), name='setup_profile'),
)