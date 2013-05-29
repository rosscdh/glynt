# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from views import PublicHomepageView, ContactUsView, \
                    UserClassSessionRedirectView, UserClassLoggedInRedirectView

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
    # Social Auth session setter for user class
    url(r'^auth-redirect/(?P<user_class_name>.+)/$', UserClassSessionRedirectView.as_view(), name='auth_user_class_redirect'),
    # Social Auth Logged-in redirect to user type homepage
    url(r'^logged-in/$', UserClassLoggedInRedirectView.as_view(), name='auth_user_class_logged_in_redirect'),
    url(r'^login-error/$', TemplateView.as_view(template_name='public/login-error.html'), name='login_error'),
    # home
    url(r'^$', PublicHomepageView.as_view(), name='homepage'),
)