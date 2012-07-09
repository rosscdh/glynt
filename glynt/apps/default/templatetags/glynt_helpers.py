from django.conf import settings
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def CURRENT_DATE_FORMAT():
    return settings.DATE_FORMAT
CURRENT_DATE_FORMAT.is_safe = True
