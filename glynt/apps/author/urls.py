from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from glynt.apps.author.views import AuthorToolView


urlpatterns = patterns('',
    # Authoring
    url(r'^(?P<pk>\d+)/$', login_required(AuthorToolView.as_view()), name='edit'),
    url(r'^$', login_required(AuthorToolView.as_view()), name='create'),
)
