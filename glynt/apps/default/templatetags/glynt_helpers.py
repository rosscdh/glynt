from django.conf import settings
from django.contrib.sites.models import Site
from django import template
import ast

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
    true_eval = (True, 'True')
    false_eval = (False, 'False')
    kwargs['STATIC_URL'] = settings.STATIC_URL
    kwargs['just_image'] = True if 'just_image' in kwargs and kwargs['just_image'] in true_eval else False
    kwargs['modal'] = False if 'modal' in kwargs and kwargs['modal'] in false_eval else True
    kwargs['header'] = False if 'header' in kwargs and kwargs['header'] in false_eval else True
    kwargs['body'] = False if 'body' in kwargs and kwargs['body'] in false_eval else True
    kwargs['footer'] = False if 'footer' in kwargs and kwargs['footer'] in false_eval else True
    return kwargs