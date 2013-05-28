# -*- coding: utf-8 -*-
from itertools import chain
from django import template
from django.template.defaultfilters import slugify

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.startup.models import Startup

import json

register = template.Library()

import logging
logger = logging.getLogger('django.request')


@register.inclusion_tag('lawyer/partials/startups_advised.html', takes_context=True)
def startups_advised(context):
    context.update({
        'lawyer': context.get('object', None),
        'startups': lawyer.startups_advised,
    })
    return context


@register.inclusion_tag('lawyer/partials/simple_name_list.html', takes_context=False)
def simple_name_list(data_list):
    context = {
        'object_list': data_list,
    }
    return context


@register.inclusion_tag('lawyer/partials/fee_packages.html', takes_context=False)
def fee_packages(lawyer):
    context = {
        'fee_package_list': lawyer.fee_packages.items()
    }
    return context