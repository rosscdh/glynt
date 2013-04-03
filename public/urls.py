from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import ProcessFormView

from glynt.apps.lawyer.forms import LawyerProfileSetupForm
from glynt.apps.lawyer.views import LawyerProfileSetupView

from views import LoggedInRedirectView


urlpatterns = patterns('',
    # about
    url(r'^about/$', TemplateView.as_view(template_name='public/about.html'), name='terms'),
    # T&C
    url(r'^terms/$', TemplateView.as_view(template_name='public/terms-and-conditions.html'), name='terms'),
    # Logged-in
    url(r'^logged-in/$', LoggedInRedirectView.as_view(), name='logged_in_generic'),
    # lawyers
    url(r'^lawyers/profile/setup/$', login_required(LawyerProfileSetupView.as_view()), name='lawyer_setup_profile'),
    url(r'^lawyers/$', login_required(TemplateView.as_view(template_name='public/lawyer-welcome.html')), name='lawyer'),
    url(r'^lawyers/thanks/$', TemplateView.as_view(template_name='public/lawyer-profile-thanks.html'), name='thanks'),
    # home
    url(r'^$', TemplateView.as_view(template_name='public/homepage.html'), name='homepage'),

)
