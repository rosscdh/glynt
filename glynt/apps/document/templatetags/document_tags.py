from django import template

from glynt.apps.document.models import DocumentTemplate, DocumentTemplateCategory

import user_streams

register = template.Library()


@register.inclusion_tag('document/partials/document_categories_home.html')
def document_categories_home():
    return {
    'objects': DocumentTemplateCategory.objects.filter(active=True)
    }


@register.inclusion_tag('document/partials/document_examples.html')
def document_examples(num=4):
    return {
        'objects': DocumentTemplate.public_objects.by_acronym()[:num]
    }


@register.inclusion_tag('document/comments/base.html')
def comments_for_object(obj, next):
    return {
    'object': obj,
    'next': next
    }


@register.inclusion_tag('document/comments/comments.js')
def comments_js():
    return {}


@register.inclusion_tag('activity/activity_list.html')
def document_activity_stream(document, user=None, limit=10):
  return {
    'object_list': user_streams.get_object_stream_items(document, user)[:limit]
  }


