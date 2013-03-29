from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView

from glynt.apps.lawyer.forms import LawyerSignupForm


urlpatterns = patterns('',
    # lawyers
    url(r'^lawyers/signup/$', FormView.as_view(template_name='public/lawyer-welcome-form.html', form_class=LawyerSignupForm), name='lawyer_signup'),
    url(r'^lawyers/$', TemplateView.as_view(template_name='public/lawyer-welcome.html'), name='lawyer'),
    # home
    url(r'^$', TemplateView.as_view(template_name='public/homepage.html'), name='homepage'),
)
