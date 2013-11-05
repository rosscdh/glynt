from django.conf.urls import patterns, url

from django.views.generic import TemplateView
from .views import HelloSignEventView


urlpatterns = patterns('',
    # lawyers
    url(r'^hellosign/event/$', HelloSignEventView.as_view(), name='hellosign_event'),
    url(r'^hellosign/$', TemplateView.as_view(template_name='sign/hellosign.html'), name='hellosign_default'),
)

