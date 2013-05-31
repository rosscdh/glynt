from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^category/(?P<type>.+)/(?P<category>.+)/$', DocumentByCategoryListView.as_view(), name='category_list'),

    # Client Created Documents
    url(r'^me/$', 'graph.views.me'),
    url(r'^(?P<pk>\d+)$', 'graph.views.connections_for_user'),
    url(r'^common/(?P<pk>\d+)/(?P<pk>\d+)/$', 'graph.views.user_to_user'),
)
