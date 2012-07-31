from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from views import SignupView, LoginView, DashboardView, HasLocalFacebookAccountView


urlpatterns = patterns('',
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),

    url(r'^has/fb/account/$', HasLocalFacebookAccountView.as_view(), name='has_fb_account'),

    url(r'^$', DashboardView.as_view(), name='dashboard'),
)
