# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType

TODO_CONTENT_TYPE = ContentType.objects.get(app_label="todo", model="todo")

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


@register.inclusion_tag('todo/stream/todo_list.html', takes_context=False)
def todo_stream(todo):
    return {
        'stream': Action.objects.filter(target_object_id=todo.pk, target_content_type=TODO_CONTENT_TYPE)
    }


@register.inclusion_tag('todo/partials/primary_interface.html', takes_context=True)
def todo_primary_interface(context, todo):
    todo = context.get('object')

    data = {
        'project': context.get('project'),
        'todo': todo,
        'user': context.get('user'),
        'back_and_forth': context.get('back_and_forth'),
        'is_lawyer': context.get('user').profile.is_lawyer,
        'is_customer': context.get('user').profile.is_customer,
        'is_new': todo.status == TODO_STATUS.new,
        'is_open': todo.status == TODO_STATUS.open,
        'is_pending': todo.status == TODO_STATUS.pending,
        'is_resolved': todo.status == TODO_STATUS.resolved,
        'is_closed': todo.status == TODO_STATUS.closed,
    }
    return data
