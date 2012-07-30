from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

import forms_builder.forms.urls

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('socialregistration.urls', namespace='socialregistration')),
    url(r'^client/', include('glynt.apps.client.urls', namespace='client')),
    # Forms for the documents
    url(r'^doc/forms/', include(forms_builder.forms.urls)),
    # The documents
    url(r'^doc/', include('glynt.apps.document.urls', namespace='document')),
    url(r'^', include('glynt.apps.default.urls', namespace='glynt')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^m/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )