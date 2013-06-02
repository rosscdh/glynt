from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from glynt.apps.api.v1 import v1_internal_api

admin.autodiscover()


urlpatterns = patterns('',
	# Admin
	url(r'^admin/', include(admin.site.urls)),
	# Api
	url(r'^api/', include(v1_internal_api.urls, namespace='api')),
    # image upload and crop
    url(r'^ajax-upload/', include('cicu.urls')),
    # Invite to join
    url(r'^invite/', include('public.invite.urls', namespace='invite')),
	# Accounts & Registration
    url(r'', include('social_auth.urls')),
	url(r'^accounts/', include('userena.urls')),
	url(r'^client/', include('glynt.apps.client.urls', namespace='client')),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    # Startups
    url(r'^startups/', include('glynt.apps.startup.urls', namespace='startup')),
    # Legal Firms
    url(r'^firms/', include('glynt.apps.firm.urls', namespace='firm')),
    # lawyers
    url(r'^lawyers/', include('glynt.apps.lawyer.urls', namespace='lawyer')),
    # Engage app
    url(r'^engage/', include('glynt.apps.engage.urls', namespace='engage')),
    # Messaging
    url(r'^messages/', include('postman.urls')),
	# Document Comments
	url(r'^doc/comments/', include('django.contrib.comments.urls')),
	# The Authoring Tool
	url(r'^author/', include('glynt.apps.author.urls', namespace='author')),
	# The v2 Documents
	url(r'^document/', include('glynt.apps.smoothe.urls', namespace='doc')),
	# The v1 Documents
	url(r'^template/', include('glynt.apps.document.urls', namespace='document')),
	# The Export
	url(r'^export/', include('glynt.apps.export.urls', namespace='export')),
	# The Document Signatures
	url(r'^sign/doc/', include('glynt.apps.sign.urls', namespace='sign')),
    # The graph
    url(r'^graph/', include('glynt.apps.graph.urls', namespace='graph')),
    # favicon
    url(r'^favicon\.ico/$', RedirectView.as_view(url='%simg/favicon.ico' % settings.STATIC_URL)),
    url(r'', include('debug_toolbar_user_panel.urls')),
	# The public site and theme
	url(r'^', include('public.urls', namespace='public')),
)


if settings.DEBUG or settings.PROJECT_ENVIRONMENT == 'dev':
	urlpatterns += staticfiles_urlpatterns()
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
