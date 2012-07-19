from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='default/index.html'), name='default'),
)
