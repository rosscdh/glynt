from django.conf import settings
from django.contrib.sites.models import Site
from django import template

register = template.Library()


@register.simple_tag
def current_date_format():
    return settings.DATE_FORMAT
current_date_format.is_safe = True


@register.simple_tag
def current_site_domain():
    site = Site.objects.get_current()
    return site.domain
current_site_domain.is_safe = True


@register.inclusion_tag('pleasewait/loading.html')
def show_loading(**kwargs):
    kwargs['STATIC_URL'] = settings.STATIC_URL
    kwargs['just_image'] = kwargs['just_image'] if 'just_image' in kwargs else False
    kwargs['modal'] = kwargs['modal'] if 'modal' in kwargs else True
    kwargs['header'] = kwargs['header'] if 'header' in kwargs else True
    kwargs['body'] = kwargs['body'] if 'body' in kwargs else True
    kwargs['footer'] = kwargs['footer'] if 'footer' in kwargs else True
    return kwargs