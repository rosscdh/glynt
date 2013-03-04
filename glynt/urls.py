from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from cms.sitemaps import CMSSitemap

from glynt.apps.api.v1 import v1_internal_api

admin.autodiscover()


urlpatterns = patterns('',
	# Admin
	url(r'^admin/', include(admin.site.urls)),
	# Api
	url(r'^api/', include(v1_internal_api.urls)),
	# Accounts & Registration
	url(r'^social/', include('socialregistration.urls', namespace='socialregistration')),
	url(r'^accounts/', include('userena.urls')),
	url(r'^client/', include('glynt.apps.client.urls', namespace='client')),
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
	# Sitemap
	url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}})
)


# Django CMS
urlpatterns += patterns('',
	url(r'^', include('cms.urls')),
)


if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()