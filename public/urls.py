from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import ProcessFormView

from glynt.apps.lawyer.forms import LawyerProfileSetupForm
from glynt.apps.lawyer.views import LawyerProfileSetupView

urlpatterns = patterns('',
    # about
    url(r'^about/$', TemplateView.as_view(template_name='public/about.html'), name='terms'),
    # T&C
    url(r'^terms/$', TemplateView.as_view(template_name='public/terms-and-conditions.html'), name='terms'),
    # lawyers
    url(r'^lawyers/setup/profile/$', login_required(LawyerProfileSetupView.as_view()), name='lawyer_setup_profile'),
    url(r'^lawyers/$', login_required(TemplateView.as_view(template_name='public/lawyer-welcome.html')), name='lawyer'),
    # home
    url(r'^$', TemplateView.as_view(template_name='public/homepage.html'), name='homepage'),
)
