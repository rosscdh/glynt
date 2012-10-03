from django import template

from glynt.apps.document.models import DocumentCategory

register = template.Library()

@register.inclusion_tag('document/partials/document_categories_home.html')
def document_categories_home():
    return {
    'objects': DocumentCategory.objects.filter(active=True)
    }


@register.inclusion_tag('document/comments/base.html')
def show_comments_for_object(obj, next):
    return {
    'object': obj,
    'next': next
    }

@register.inclusion_tag('document/comments/comments.js')
def comments_js():
    return {}
