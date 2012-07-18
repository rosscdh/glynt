from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from views import DashboardView


urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
)
