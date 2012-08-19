from django.conf import settings
from django import template

register = template.Library()

@register.simple_tag
def current_date_format():
    return settings.DATE_FORMAT
current_date_format.is_safe = True
