from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    # startups
    url(r'^sign-up/$', TemplateView.as_view(template_name='startup/sign-up-form.html'), name='startup_signup_form'),
)