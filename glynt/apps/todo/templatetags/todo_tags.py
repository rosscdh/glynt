# -*- coding: utf-8 -*-
from django import template

from glynt.apps.todo import TODO_STATUS

register = template.Library()

STATUS_CLASSES = {
    TODO_STATUS.closed: 'closed',
    TODO_STATUS.unassigned: 'closed',
    TODO_STATUS.assigned: 'assigned',
}

STATUS_ICONS = {
    TODO_STATUS.closed: 'icon-ok-sign',
    TODO_STATUS.unassigned: 'icon-screenshot',
    TODO_STATUS.assigned: 'icon-wrench',
}


@register.filter
def todo_status_row_class(value):
    return STATUS_CLASSES.get(value, 'pending')
todo_status_row_class.is_safe = True


@register.filter
def todo_status_icon(value):
    return STATUS_ICONS.get(value, 'icon-pending')
todo_status_icon.is_safe = True
