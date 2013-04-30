# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from social_auth.views import auth, complete, disconnect

from views import ConfirmLoginDetailsView, SignupView, LoginView, DashboardView
from glynt.decorators import anonymous_required


urlpatterns = patterns('',
    url(r'^signup/$', anonymous_required(SignupView.as_view()), name='signup'),
    url(r'^signup/(?P<slug>.+)/confirm/$', login_required(ConfirmLoginDetailsView.as_view()), name='confirm_signup'),
    url(r'^login/$', anonymous_required(LoginView.as_view()), name='login'),
    url(r'^$', login_required(DashboardView.as_view()), name='dashboard'),
)
