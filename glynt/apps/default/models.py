# -*- coding: utf-8 -*-
from glynt.apps.utils import CURRENT_SITE
from threadedcomments.models import ThreadedComment
from taggit.managers import TaggableManager


import cities_light


def filter_city_import(sender, items, **kwargs):
    if items[8] not in ('GB', 'US', 'DE', 'IL', 'AU', 'CA'):
        raise cities_light.InvalidItems()

cities_light.signals.city_items_pre_import.connect(filter_city_import)


"""
Patch the django-rulez permissions on to our 
Threadedcomment Class.

Patch django-taggit
"""
def threadedcomment_can_read(self, **kwargs):
    project = self.content_object
    user = kwargs.get('user')
    return project.can_read(user=user)

def threadedcomment_can_edit(self, **kwargs):
    project = self.content_object
    user = kwargs.get('user')
    return project.can_edit(user=user)

def threadedcomment_can_delete(self, **kwargs):
    project = self.content_object
    user = kwargs.get('user')
    return project.can_delete(user=user)

def threadedcomment_absolute_deeplink_url(self, **kwargs):
    if not hasattr(self.content_object, 'get_absolute_url'):
        return None
    else:
        # we have an absolute url
        parent_id = self.parent_id if self.parent_id is not None else self.pk
        return '{path}#/discussion/{parent_id}'.format(path=self.content_object.get_absolute_url(),
                                                            parent_id=parent_id)

ThreadedComment.add_to_class('can_read', threadedcomment_can_read)
ThreadedComment.add_to_class('can_edit', threadedcomment_can_edit)
ThreadedComment.add_to_class('can_delete', threadedcomment_can_delete)

ThreadedComment.add_to_class('absolute_deeplink_url', threadedcomment_absolute_deeplink_url)

ThreadedComment.add_to_class('tags', TaggableManager(blank=True))


"""
Import our on_user_logged_in
"""
from .signals import on_user_logged_in
