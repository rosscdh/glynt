from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from glynt.apps.sign.views import ProcessInviteToSignView, SignDocumentView, ProcessSignDocumentView, RenderSignatureImageView
from glynt.apps.sign.views import DeleteInviteToSignView


urlpatterns = patterns('',
  # Invitation view, posted to from javascript widget
  url(r'^(?P<pk>\d+)/invite/$', ProcessInviteToSignView.as_view(), name='process_invite'),
  url(r'^(?P<pk>\d+)/invite/complete/$', TemplateView.as_view(template_name='sign/invite_complete.html'), name='invite_complete'),
  url(r'^(?P<pk>\d+)/(?P<invitation_pk>\d+)/delete/$', DeleteInviteToSignView.as_view(), name='delete_invite'),

  # Invitee pages, where the invitee has the option to sign the document
  # pk here refers to the document_pk and not the signature_pk @TODO double check this
  url(r'^(?P<pk>\d+)/(?P<hash>\w+)/sign/$', ProcessSignDocumentView.as_view(), name='process_signature'),
  url(r'^(?P<pk>\d+)/(?P<hash>\w+)/signature/$', RenderSignatureImageView.as_view(), name='signature_pic'),
  url(r'^(?P<pk>\d+)/(?P<hash>\w+)/$', SignDocumentView.as_view(), name='default'),
)
