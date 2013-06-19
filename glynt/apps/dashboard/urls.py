from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^checklist/(?P<id>[a-zA-Z0-9]{24})$', TemplateView.as_view(template_name='dashboard/item.html'), name='item'),
    url(r'^checklist$', TemplateView.as_view(template_name='dashboard/checklist.html'), name='checklist'),
    url(r'^documents$', TemplateView.as_view(template_name='dashboard/documents.html'), name='documents'),
    url(r'^$', TemplateView.as_view(template_name='dashboard/overview.html'), name='overview'),
)
