# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import redirect

from glynt.apps.default.views import ManualLoginView

from views import (PublicHomepageView, ContactUsView,
                    UserClassSessionRedirectView, 
                    UserClassLoggedInRedirectView,
                    CustomerStartView, LawyerStartView)

urlpatterns = patterns('',
    # about
    url(r'^about/$', TemplateView.as_view(template_name='public/about.html'), name='about'),
    # lawyers
    url(r'^lawyers/$', TemplateView.as_view(template_name='public/lawyers.html'), name='lawyers'),
    # T&C
    url(r'^legal/terms/$', TemplateView.as_view(template_name='public/terms-and-conditions.html'), name='terms'),
    # Privacy
    url(r'^legal/privacy-policy/$', TemplateView.as_view(template_name='public/privacy-policy.html'), name='privacy'),
    # T&C
    url(r'^legal/disclaimer/$', TemplateView.as_view(template_name='public/disclaimer.html'), name='disclaimer'),
    # Contact us
    url(r'^contact-us/$', ContactUsView.as_view(), name='contact_us'),

    # 
    url(r'^why-lawpal/$', TemplateView.as_view(template_name='public/why-lawpal.html'), name='why-lawpal'),
    url(r'^must-reads/$', TemplateView.as_view(template_name='public/must-reads.html'), name='must-reads'),
    url(r'^for-lawyers/$', TemplateView.as_view(template_name='public/for-lawyers.html'), name='for-lawyers'),

    # Start
    url(r'^start/$', CustomerStartView.as_view(), name='start'),
    url(r'^start/lawyer/$', LawyerStartView.as_view(), name='start-lawyer'),

    # Social Auth session setter for user class
    url(r'^auth-redirect/(?P<user_class_name>.+)/(?P<login_type>.+)/$', UserClassSessionRedirectView.as_view(), name='auth_user_class_redirect'),
    # Social Auth Logged-in redirect to user type homepage
    url(r'^logged-in/$', UserClassLoggedInRedirectView.as_view(), name='auth_user_class_logged_in_redirect'),
    url(r'^login-error/$', TemplateView.as_view(template_name='public/login-error.html'), name='login_error'),

    url(r'^sorry-you-are-a-lawyer/$', TemplateView.as_view(template_name='public/sorry_are_lawyer.html'), name='sorry_are_lawyer'),
    url(r'^sorry-you-are-a-customer/$', TemplateView.as_view(template_name='public/sorry_are_customer.html'), name='sorry_are_customer'),

    # manual login
    url(r'^l/$', ManualLoginView.as_view(), name='login'),

    # home
    url(r'^$', PublicHomepageView.as_view(), name='homepage'),
)