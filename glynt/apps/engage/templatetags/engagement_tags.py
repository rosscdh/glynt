# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.db.models import Count

register = template.Library()

from notifications.models import Notification

from glynt.apps.engage.models import Engagement
from glynt.apps.engage.utils import ENGAGEMENT_CONTENT_TYPE


@register.inclusion_tag('engage/partials/engagement_intro.html', takes_context=True)
def engagement_intro(context, enagement):
    context.update({
        'enagement': enagement,
    })
    return context


def engagement_dict(context, user=None):
    engagements = []
    user = context.get('user', user)
    lawyer = context.get('lawyer', None)
    is_own_profile = True if lawyer.user.pk == user.pk else False

    if user is not None:
        if user.is_authenticated():
            if not is_own_profile:
                if user.profile.is_founder:
                    engagements = Engagement.objects.filter(lawyer=lawyer, founder=user.founder_profile)

    return {
        'engagements': engagements,
        'num_engagements': len(engagements),
        'is_own_profile' : is_own_profile,
    }


@register.inclusion_tag('engage/partials/engagement_with_lawyer.html', takes_context=True)
def engagement_with_lawyer(context, lawyer):
    context.update({
        'lawyer': lawyer,
    })

    context.update(
        engagement_dict(context)
    )

    return context



@register.inclusion_tag('engage/partials/engage_with_lawyer_button.html', takes_context=True)
def engage_with_lawyer_button(context, lawyer=None, user=None):
    lawyer_enganged = False
    user = context.get('user', user)
    lawyer = context.get('lawyer', lawyer)
    data = {}
    data.update({
        'lawyer': lawyer,
    })
    data.update(engagement_dict(context=context, user=user))
    data.update({
        'has_engagements': True if data.get('engagements') else False,
    })
    context.update(data)
    return context


@register.inclusion_tag('engage/partials/user_engagement_notification_count.js', takes_context=False)
def user_engagement_notification_count(user):
    unread = {}
    
    # get a grouped by result set
    unread_qs = Notification.objects.filter(recipient=user, unread=True, target_content_type=ENGAGEMENT_CONTENT_TYPE)

    # build a nice jsonifyable dict
    for u in unread_qs:
        # target_object_id is the id of the content object (engagement)
        if u.target_object_id not in unread:
            unread[u.target_object_id] = unread.get(u.target_object_id, 1)
        else:
            unread[u.target_object_id] += 1
    return {
        'unread': unread
    }