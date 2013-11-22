from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

from rest_framework.routers import DefaultRouter

from django.views.generic import TemplateView

from .views import HelloSignEventView, HelloSignSignatureView
from .api_v2 import SignatureViewSet

# pattern for the api
api_router = DefaultRouter()
api_router.register(r'signature', SignatureViewSet)

# standard urls
urlpatterns = patterns('',
    # lawyers
    url(r'^hellosign/event/$', csrf_exempt(HelloSignEventView.as_view()), name='hellosign_event'),
    url(r'^hellosign/(?P<pk>\d+)/$', xframe_options_exempt(HelloSignSignatureView.as_view()), name='signature'),
    url(r'^hellosign/$', TemplateView.as_view(template_name='hellosign/hellosign.html'), name='hellosign_default'),
)

