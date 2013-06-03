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


def engagement_dict(data):
    engagement_list = []
    own_profile = True if data.get('lawyer').user.pk == data.get('user').pk else False

    if data.get('user',None) is not None:
        if not own_profile:
            if data.get('user').profile.is_startup:
                engagement_list = Engagement.objects.filter(lawyer=data.get('lawyer'), founder=data.get('user').founder_profile)

    data = {
        'engagement_list': engagement_list,
        'own_profile' : own_profile,
    }

    return data


@register.inclusion_tag('engage/partials/engagement_with_lawyer.html', takes_context=True)
def engagement_with_lawyer(context, lawyer):

    context.update({
        'lawyer': lawyer,
    })

    context.update(
        engagement_dict(context)
    )

    return context


@register.assignment_tag(takes_context=True)
def is_lawyer_engaged(context, lawyer):
    context.update({
        'lawyer': lawyer,
    })

    lawyer_enganged = False
    data = engagement_dict(context)

    if data.get('engagement_list'):
        lawyer_enganged = True

    return lawyer_enganged