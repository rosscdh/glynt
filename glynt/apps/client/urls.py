from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from views import SignupView, LoginView, DashboardView, HasLocalFacebookAccountView
from glynt.decorators import anonymous_required


urlpatterns = patterns('',
    url(r'^signup/$', anonymous_required(SignupView.as_view()), name='signup'),
    url(r'^login/$', anonymous_required(LoginView.as_view()), name='login'),

    url(r'^has/fb/account/$', HasLocalFacebookAccountView.as_view(), name='has_fb_account'),

    url(r'^$', login_required(DashboardView.as_view()), name='dashboard'),
)
