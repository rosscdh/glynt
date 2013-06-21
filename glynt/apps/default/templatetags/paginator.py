# -*- coding: utf-8 -*-
from django import template

register = template.Library()

import logging
logger = logging.getLogger('django.request')


@register.inclusion_tag('partials/pagination.html', takes_context=True)
def paginator(context, object_list):
    current_page = int(context.get('request').GET.get('page', 1))
    #tabs = [current_page + page_num for page_num,todo in enumerate(object_list[current_page:5])]

    context.update({
        'object_list': object_list,
        #'tabs': tabs,
    })
    return context