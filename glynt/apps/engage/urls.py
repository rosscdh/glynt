# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from views import EngageWriteMessageView

urlpatterns = patterns('',
    # enage message
    url(r'^(?P<to>.+)/message/$', EngageWriteMessageView.as_view(), name='message'),
)