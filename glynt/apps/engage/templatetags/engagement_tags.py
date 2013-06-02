# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.inclusion_tag('engage/partials/engagement_intro.html', takes_context=True)
def engagement_intro(context, enagement):
    context.update({
        'enagement': enagement,
    })
    return context
