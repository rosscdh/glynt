# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from public.invite.forms import InviteEmailForm

register = template.Library()


@register.filter
def todo_status_row_class(value):
    return "pending"
todo_status_row_class.is_safe = True


@register.filter
def todo_status_icon(value):
    return "icon-pending"
todo_status_icon.is_safe = True