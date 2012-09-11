from django.conf.urls import patterns, url
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required

from glynt.apps.sign.views import DocumentSignatureView, DocumentSignatureInviteToSignView


urlpatterns = patterns('',
  url(r'^(?P<pk>\d+)/invite/$', DocumentSignatureInviteToSignView.as_view(), name='invite'),
  url(r'^(?P<pk>\d+)/complete/$', DocumentSignatureView.as_view(template_name='sign/complete.html'), name='complete'),
  url(r'^(?P<pk>\d+)/(?P<hash>\w+)/$', DocumentSignatureView.as_view(), name='default'),
)
