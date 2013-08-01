# -*- coding: utf-8 -*-
from django import template

from glynt.apps.todo import TODO_STATUS

register = template.Library()

STATUS_CLASSES = {
    TODO_STATUS.closed: 'complete',
    TODO_STATUS.unassigned: 'pending',
    TODO_STATUS.assigned: 'urgent',
}

STATUS_ICONS = {
    TODO_STATUS.closed: 'icon-complete',
    TODO_STATUS.unassigned: 'icon-pending',
    TODO_STATUS.assigned: 'icon-urgent',
}


@register.filter
def todo_status_row_class(value):
    return STATUS_CLASSES.get(value, 'pending')
todo_status_row_class.is_safe = True


@register.filter
def todo_status_icon(value):
    return STATUS_ICONS.get(value, 'icon-pending')
todo_status_icon.is_safe = True
