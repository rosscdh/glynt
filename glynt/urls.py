from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    # Accounts & Registration
    url(r'^social/', include('socialregistration.urls', namespace='socialregistration')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^client/', include('glynt.apps.client.urls', namespace='client')),
    # The Documents
    url(r'^doc/', include('glynt.apps.document.urls', namespace='document')),
    # The Document Signatures
    url(r'^sign/doc/', include('glynt.apps.sign.urls', namespace='sign')),
    # Default App
    url(r'^', include('glynt.apps.default.urls', namespace='glynt')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^m/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )