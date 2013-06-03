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


@register.inclusion_tag('engage/partials/engagement_with_lawyer.html', takes_context=True)
def engagement_with_lawyer(context, lawyer):
    engagement_list = []
    own_profile = True if lawyer.user.pk == context.get('user').pk else False

    if context.get('user',None) is not None:
        if not own_profile:
            if context.get('user').profile.is_startup:
                engagement_list = Engagement.objects.filter(lawyer=lawyer, founder=context.get('user').founder_profile)

    context.update({
        'engagement_list': engagement_list,
        'own_profile': own_profile,
        'lawyer': lawyer,
    })
    return context


@register.assignment_tag(takes_context=True)
def is_lawyer_engaged(context, lawyer):
    lawyer_enganged = False

    own_profile = True if lawyer.user.pk == context.get('user').pk else False

    if context.get('user',None) is not None:
        if not own_profile:
            if context.get('user').profile.is_startup:
                lawyer_enganged = True if Engagement.objects.filter(lawyer=lawyer, founder=context.get('user').founder_profile) else False

    return lawyer_enganged