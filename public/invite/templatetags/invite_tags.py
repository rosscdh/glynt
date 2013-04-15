# -*- coding: utf-8 -*-
from django import template

from public.invite.forms import InviteEmailForm

register = template.Library()


@register.inclusion_tag('invite/invite.html', takes_context=True)
def invite_to_lawpal(context, invite_type):
    return {
        'form': InviteEmailForm(initial={'invite_type': invite_type})
        ,'STATIC_URL': context['STATIC_URL']
    }
