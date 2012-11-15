from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required



urlpatterns = patterns('',
    url(r'^my/(?P<slug>.+)/$', login_required(TemplateView.as_view(template_name='smoothe/document.html')), name='view'),
)
