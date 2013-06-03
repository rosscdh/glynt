# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

from glynt.apps.engage.models import Engagement


@register.inclusion_tag('engage/partials/engagement_intro.html', takes_context=True)
def engagement_intro(context, enagement):
    context.update({
        'enagement': enagement,
    })
    return context


def get_engagement_list(data, lawyer):
    engagement_list = []
    own_profile = True if lawyer.user.pk == data.get('user').pk else False

    if data.get('user',None) is not None:
        if not own_profile:
            if data.get('user').profile.is_startup:
                engagement_list = Engagement.objects.filter(lawyer=lawyer, founder=data.get('user').founder_profile)

    data = {
        'engagement_list': engagement_list,
        'own_profile' : own_profile,
    }

    return data


@register.inclusion_tag('engage/partials/engagement_with_lawyer.html', takes_context=True)
def engagement_with_lawyer(context, lawyer):
    data = get_engagement_list(context, lawyer)

    context.update({
        'engagement_list': data.get('engagement_list'),
        'own_profile': data.get('own_profile'),
        'lawyer': lawyer,
    })
    return context


@register.assignment_tag(takes_context=True)
def is_lawyer_engaged(context, lawyer):
    lawyer_enganged = False
    data = get_engagement_list(context, lawyer)

    if data.get('engagement_list'):
        lawyer_enganged = True

    return lawyer_enganged