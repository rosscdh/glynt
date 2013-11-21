# -*- coding: UTF-8 -*-
"""
Mixins that relate to the Project app
"""
from collections import OrderedDict

from glynt.apps.todo.models import ToDo


class ProjectRulezMixin(object):
    """
    Mixin to use django-rulez with Project model
    needs to register the methods
    >> registry.register("can_read", Project)
    >> registry.register("can_edit", Project)
    >> registry.register("can_delete", Project)
    """
    def can_read(self, user):
        return True if user.pk in [u.pk for u in self.notification_recipients()] else False

    def can_edit(self, user):
        editors = [self.customer.user] + list([l.user for l in self.lawyers.all()])
        return True if user.pk in [u.pk for u in editors] else False

    def can_delete(self, user):
        editors = [self.customer.user] + list([l.user for l in self.lawyers.all()])
        return True if user.pk in [u.pk for u in editors] else False


class ProjectCategoriesMixin(object):
    """
    A mixin specifically and only for Project ORM objects
    That allows us to store in the .data JSON object the categories
    associated with this Project.data Object
    """
    @property
    def categories(self):
        category_order = self.data.get('category_order', [])
        if category_order:
            #return ordered categories
            return category_order
        else:
            # get the default set of categories
            return self.original_categories

    @categories.setter
    def categories(self, value):
        if type(value) is list:
            self.data['category_order'] = value

    @property
    def original_categories(self):
        # get a set of original categories in the order of creation
        return list(set(OrderedDict.fromkeys([todo.category for todo in self.todo_set.all()])))

    def delete_categories(self, delete_categories):
        # ensure we have a list of at least 1
        delete_categories = [delete_categories] if type(delete_categories) not in [list] else delete_categories

        # rebuild the list based on wether its in the list or not
        # update with our new filtered list
        self.categories = [c for c in self.categories if c not in delete_categories]

        # delete category items
        self.delete_items_by_category(delete_categories=delete_categories)

    def delete_items_by_category(self, delete_categories):
        # ensure we have an array
        delete_categories = [delete_categories] if type(delete_categories) not in [list] else delete_categories

        # select set and update is_deleted
        self.todo_set.filter(category__in=delete_categories).update(is_deleted=True)


class ProjectActivityMixin(object):
    """
    A Mixin to collect the project and its related items "action" objects
    1. project
    2. todo items (and by association their attachments, 
       attachments comments is setup to comment on the todo item and not the attachment itself)
    """
    def activity_stream(self, **kwargs):
        from actstream.models import Action
        # return the combined queryset of the selection for the current project actions
        # as well as the todo items related to the project
        return Action.objects.prefetch_related('actor').filter(target_object_id=self.pk,
                                     target_content_type=self.content_type(), **kwargs) | \
                Action.objects.prefetch_related('actor').filter(target_object_id__in=[p[0] for p in self.todo_set.all().values_list('pk')],
                                     target_content_type=ToDo.content_type(), **kwargs)
