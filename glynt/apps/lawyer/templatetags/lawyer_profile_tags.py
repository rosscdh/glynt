# -*- coding: utf-8 -*-
from itertools import chain
from django import template
from django.template.defaultfilters import slugify

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.lawyer.forms import LawyerProfileIsCompleteValidator
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

@register.inclusion_tag('lawyer/partials/fee_packages_mini.html', takes_context=False)
def fee_packages_mini(fee_packages):
    context = {
        'fee_package_list': fee_packages
    }
    return context

@register.filter(takes_context=False)
def humanise_number(num):
    if not isinstance(num, ( int, long )):
        num = 0
        logger.debug('Value "num" passed to humanise_number must be a number is type: %s %s' % (type(num),num,))

    magnitude = 0

    while num >= 1000:
        magnitude += 1
        num /= 1000

    humanised_num = '%s%s' % (num, ['', 'k', 'm', 'g', 't', 'p'][magnitude])
    return humanised_num


@register.inclusion_tag('lawyer/partials/profile_is_complete.html', takes_context=True)
def lawyer_profile_is_complete(context, lawyer=None):
    lawyer = lawyer if lawyer is not None else context.get('lawyer', None)
    if lawyer is None:
        raise Exception('lawyer_profile_is_complete requires a lawyer to be present in the context or to be passed in')
    profile_form = LawyerProfileIsCompleteValidator({
        'first_name': lawyer.user.first_name,
        'last_name': lawyer.user.last_name,
        'firm_name': lawyer.firm_name,
        'phone': lawyer.phone,
        'position': lawyer.position,
        'years_practiced': lawyer.years_practiced,
        'practice_location_1': lawyer.data.get('practice_location_1', None),
        'fee_packages': ','.join([p.key for p in lawyer.fee_packages.items()]),
        'summary': lawyer.summary,
    })

    context.update({
        'profile_is_valid': profile_form.is_valid(),
        'profile_status': lawyer.profile_status,
        'is_active': lawyer.is_active,
    })
    return context