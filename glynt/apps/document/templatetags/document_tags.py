from django.conf import settings
from django import template
from django.utils.safestring import mark_safe

from glynt.apps.document.models import DocumentCategory

register = template.Library()

@register.inclusion_tag('document/partials/document_categories_home.html')
def document_categories_home():
    objects = DocumentCategory.objects.filter(active=True)
    return {
    'objects': objects
    }
