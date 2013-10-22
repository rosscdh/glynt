# -*- coding: utf-8 -*-
from threadedcomments.models import ThreadedComment
import cities_light


def filter_city_import(sender, items, **kwargs):
    if items[8] not in ('GB', 'US', 'DE', 'IL', 'AU', 'CA'):
        raise cities_light.InvalidItems()

cities_light.signals.city_items_pre_import.connect(filter_city_import)




"""
Patch the django-rulez permissions on to our 
Threadedcomment Class
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


ThreadedComment.add_to_class('can_read', threadedcomment_can_read)
ThreadedComment.add_to_class('can_edit', threadedcomment_can_edit)
ThreadedComment.add_to_class('can_delete', threadedcomment_can_delete)