# -*- coding: utf-8 -*-
"""
ToDo item signals
"""
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from actstream import action
from glynt.apps.todo.models import ToDo
from glynt.apps.todo.models import FeedbackRequest
from glynt.apps.utils import generate_unique_slug
from glynt.apps.services.pusher import PusherPublisherService

from glynt.apps.todo import TODO_STATUS, TODO_STATUS_ACTION

import logging
logger = logging.getLogger('django.request')


def is_data_field_update(**kwargs):
    update_fields = kwargs.get('update_fields', frozenset())

    # if we have a specific update that is the sort_position changed update
    # then do nothing
    if type(update_fields) is frozenset and len(update_fields) == 1 and 'data' in update_fields:
        # Do absolutely nothing
        return True
    return False


def is_sort_order_update(**kwargs):
    update_fields = kwargs.get('update_fields', frozenset())

    # if we have a specific update that is the sort_position changed update
    # then do nothing
    if type(update_fields) is frozenset and len(update_fields) == 1 and 'sort_position' in update_fields:
        # Do absolutely nothing
        return True
    return False


def get_todo_info_object(todo):
    return {
        'instance': {
            'pk': todo.pk,
            'slug': todo.slug,
            'name': todo.name,
            'category': todo.category,
            'project': {'pk': todo.project.pk},
            'display_status': todo.display_status,
            'status': todo.status,
            'is_deleted': todo.is_deleted,
            'uri': todo.get_absolute_url(),
        }
    }


@receiver(post_save, sender=ToDo, dispatch_uid='todo.item_crud')
def todo_item_crud(sender, **kwargs):
    is_new = kwargs.get('created', False)
    instance = kwargs.get('instance')

    if is_sort_order_update(**kwargs) is False and is_data_field_update(**kwargs) is False:

        info_object = get_todo_info_object(todo=instance)
        pusher_service = PusherPublisherService(channel=instance.project.pusher_id, event='todo.post_save')

        if is_new is True:
            pusher_service.event = 'todo.is_new'
            comment = label = 'Created new item "{name}"'.format(name=instance.name)

        elif instance.is_deleted is True:
            pusher_service.event = 'todo.is_deleted'
            comment = label = 'Deleted "{name}"'.format(name=instance.name)

        else:
            pusher_service.event = 'todo.is_updated'
            comment = label = 'Updated "{name}"'.format(name=instance.name)

        pusher_service.process(label=label, comment=comment, **info_object)


@receiver(pre_save, sender=ToDo, dispatch_uid='todo.status_change')
def todo_item_status_change(sender, **kwargs):
    instance = kwargs.get('instance')

    if instance.pk is None:

        # ensure the slug is present
        if instance.slug in [None, '']:
            instance.slug = generate_unique_slug(instance=instance)

            # @BUSINESSRULE ensure we have a sort_position
            if not instance.sort_position:
                instance.sort_position = instance.project.todo_set.all().count() + 1

            # @BUSINESSRULE ensure we have a sort_position_by_cat
            if not instance.sort_position_by_cat:
                instance.sort_position_by_cat = instance.sort_position

    else:

        if instance.user is not None:

            # we have an existing item
            prev_instance = ToDo.objects.get(pk=instance.pk)

            if prev_instance.status != instance.status:

                event_action = TODO_STATUS_ACTION[instance.status]
                verb = '{user} {action} the checklist item "{name}"'.format(name=instance.name, action=event_action, user=instance.user.get_full_name())

                action.send(instance.user,
                            verb=verb,
                            action_object=instance,
                            target=instance,
                            content=None,
                            event_action=event_action,
                            event='todo.status_change',
                            **get_todo_info_object(todo=instance))

                if instance.status in [TODO_STATUS.closed, TODO_STATUS.resolved]:
                    """
                    @BUSINESS RULE Update the FeedbackRequest objects that are currently open to closed
                    """
                    FeedbackRequest.objects.close_by_todo(todo=instance)