from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.flyform.author.views import AuthorToolView


urlpatterns = patterns('',
    # Authoring
    url(r'^(?P<pk>\d+)/$', login_required(AuthorToolView.as_view()), name='edit'),
    url(r'^$', login_required(AuthorToolView.as_view()), name='create'),
)
