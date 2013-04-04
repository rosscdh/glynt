from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from views import LoggedInRedirectView, PublicHomepageView


urlpatterns = patterns('',
    # about
    url(r'^about/$', TemplateView.as_view(template_name='public/about.html'), name='terms'),
    # T&C
    url(r'^terms/$', TemplateView.as_view(template_name='public/terms-and-conditions.html'), name='terms'),
    # Logged-in
    url(r'^logged-in/$', LoggedInRedirectView.as_view(), name='logged_in_generic'),
    # home
    url(r'^$', PublicHomepageView.as_view(), name='homepage'),
)
