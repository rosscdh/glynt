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
