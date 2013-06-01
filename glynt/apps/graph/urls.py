from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Graph Views
    url(r'^me/$', 'graph.views.me'),
    url(r'^(?P<pk>\d+)$', 'graph.views.connections_for_user'),
    url(r'^common/(?P<pk>\d+)/(?P<pk>\d+)/$', 'graph.views.user_to_user'),
)
