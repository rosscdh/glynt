# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

# from views import PackagesWizard, FORMS

urlpatterns = patterns('',
    # url(r'^create/$', login_required(PackagesWizard.as_view(FORMS)), name='packages'),
)