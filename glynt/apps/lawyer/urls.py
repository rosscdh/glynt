from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from glynt.apps.lawyer.forms import LawyerProfileSetupForm
from glynt.apps.lawyer.views import LawyerProfileSetupView


urlpatterns = patterns('',
    # lawyers
    url(r'^profile/setup/$', login_required(LawyerProfileSetupView.as_view()), name='setup_profile'),
    url(r'^profile/thanks/$', login_required(TemplateView.as_view(template_name='lawyer/profile-thanks.html')), name='thanks'),
    url(r'^profile/invite/$', login_required(TemplateView.as_view(template_name='lawyer/invite.html')), name='invite'),
    url(r'^$', login_required(TemplateView.as_view(template_name='lawyer/welcome.html')), name='default'),

)

