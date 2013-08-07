# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType

from actstream.models import Action

from glynt.apps.todo import TODO_STATUS

register = template.Library()

STATUS_CLASSES = {
    TODO_STATUS.new: 'state-new',
    TODO_STATUS.open: 'state-open',
    TODO_STATUS.pending: 'state-pending',
    TODO_STATUS.resolved: 'state-resolved',
    TODO_STATUS.closed: 'state-closed',
}

STATUS_ICONS = {
    TODO_STATUS.new: 'icon-state-new',
    TODO_STATUS.open: 'icon-state-open',
    TODO_STATUS.pending: 'icon-state-pending',
    TODO_STATUS.resolved: 'icon-state-resolved',
    TODO_STATUS.closed: 'icon-state-closed',
}


@register.filter
def todo_status_row_class(value):
    return STATUS_CLASSES.get(value, 'state-new')
todo_status_row_class.is_safe = True


@register.filter
def todo_status_icon(value):
    return STATUS_ICONS.get(value, 'icon-state-new')
todo_status_icon.is_safe = True


@register.filter
def todo_status_assignedto_class(todo_user):
    return 'assigned-to-user' if todo_user not in [None, ''] else ''


@register.inclusion_tag('todo/stream/todo_list.html', takes_context=False)
def todo_stream(todo):
    todo_content_type = ContentType.objects.get(app_label="todo", model="todo")
    return {
        'stream': Action.objects.filter(action_object_object_id=todo.pk, action_object_content_type=todo_content_type)
    }
