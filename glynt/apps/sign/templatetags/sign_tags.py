from django import template

from glynt.apps.document.models import DocumentCategory

register = template.Library()

@register.inclusion_tag('sign/partials/invite_to_sign.html')
def invite_to_sign(target_element):
    return {
    'target_element': target_element
    }
