# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from glynt.apps.api.v1 import V1_INTERNAL_API

admin.autodiscover()


urlpatterns = patterns('',
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Api
    url(r'^api/', include(V1_INTERNAL_API.urls, namespace='api')),

    # image upload and crop
    url(r'^ajax-upload/', include('cicu.urls')),

    # Invite to join
    url(r'^invite/', include('public.invite.urls', namespace='invite')),

    # Accounts & Registration
    url(r'', include('social_auth.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^client/', include('glynt.apps.client.urls', namespace='client')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    # Activity stream
    url('^activity/', include('actstream.urls')),

    # Crocdoc Webhook Callbacks
    url('^crocdoc/', include('glynt.apps.crocdoc.urls', namespace='crocdoc')),

    # Customers
    url(r'^customers/', include('glynt.apps.customer.urls', namespace='customer')),

    # lawyers
    url(r'^lawyers/', include('glynt.apps.lawyer.urls', namespace='lawyer')),

    # Project app
    url(r'^projects/', include('glynt.apps.project.urls', namespace='project')),

    # ToDo checklist items
    url(r'^todo/', include('glynt.apps.todo.urls', namespace='todo')),

    # Transaction
    url(r'^transact/', include('glynt.apps.transact.urls', namespace='transact')),

    # Comments
    url(r'^comments/', include('fluent_comments.urls')),

    # Dashboard
    url(r'^dashboard/', include('glynt.apps.dashboard.urls', namespace='dashboard')),

    # The public site and theme
    url(r'^', include('public.urls', namespace='public')),

    # favicon & Utils
    url(r'^favicon\.ico/$', RedirectView.as_view(url='%simg/favicon.ico' % settings.STATIC_URL)),
    url(r'', include('debug_toolbar_user_panel.urls')),
)


if settings.DEBUG or settings.PROJECT_ENVIRONMENT == 'dev':
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
