from django import template

from glynt.apps.document.models import DocumentCategory

register = template.Library()

@register.inclusion_tag('document/partials/document_categories_home.html')
def document_categories_home():
    return {
    'objects': DocumentCategory.objects.filter(active=True)
    }
