from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView
from .views import HelloSignEventView


urlpatterns = patterns('',
    # lawyers
    url(r'^hellosign/event/$', csrf_exempt(HelloSignEventView.as_view()), name='hellosign_event'),
    url(r'^hellosign/$', TemplateView.as_view(template_name='sign/hellosign.html'), name='hellosign_default'),
)

