# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from glynt.apps.firm.views import CreateFirmView


urlpatterns = patterns('',
    # Authoring
    url(r'^create/$', login_required(CreateFirmView.as_view()), name='create'),
)
