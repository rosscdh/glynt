# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from views import LoggedInRedirectView, PublicHomepageView, ContactUsView

urlpatterns = patterns('',
    # about
    url(r'^about/$', TemplateView.as_view(template_name='public/about.html'), name='about'),
    # T&C
    url(r'^legal/terms/$', TemplateView.as_view(template_name='public/terms-and-conditions.html'), name='terms'),
    # Privacy
    url(r'^legal/privacy-policy/$', TemplateView.as_view(template_name='public/privacy-policy.html'), name='privacy'),
    # T&C
    url(r'^legal/disclaimer/$', TemplateView.as_view(template_name='public/disclaimer.html'), name='disclaimer'),
    # Contact us
    url(r'^contact-us/$', ContactUsView.as_view(), name='contact_us'),
    # Logged-in
    url(r'^logged-in/$', LoggedInRedirectView.as_view(), name='logged_in_generic'),
    # home
    url(r'^$', PublicHomepageView.as_view(), name='homepage'),
)