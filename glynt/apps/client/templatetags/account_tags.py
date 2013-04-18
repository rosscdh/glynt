# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from public.invite.forms import InviteEmailForm

register = template.Library()


@register.inclusion_tag('client/partials/social-associate.html', takes_context=True)
def social_associate(context, social_auth):
    context.update({
        'social_auth': social_auth
    })
    return context


@register.inclusion_tag('client/partials/social-button.html', takes_context=True)
def social_button(context, name, img=None, **kwargs):

    display_name = kwargs.get('display_name', None)
    social_auth = context.get('social_auth', None)

    context.update({
        'name': name,
        'display_name': display_name,
        'is_linked': social_auth.get(name, None) is not None,
        'connect_url': reverse('socialauth_begin', kwargs={'backend': name}),
        'disconnect_url': reverse('socialauth_disconnect', kwargs={'backend': name}),
        'img': img
    })
    return context