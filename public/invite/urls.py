from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import InviteEmailView


urlpatterns = patterns('',
    # lawyers
    url(r'^send/$', login_required(InviteEmailView), name='send'),
)

