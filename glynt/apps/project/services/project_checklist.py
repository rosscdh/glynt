# -*- coding: UTF-8 -*-
from django import template

from glynt.apps.todo import TODO_STATUS
from glynt.apps.project.bunches import ProjectIntakeFormIsCompleteBunch

from glynt.apps.project.services.mixins import (UserFeedbackRequestMixin,
                                                ToDoItemsFromYamlMixin,
                                                JavascriptRegionCloneMixin,
                                                ToDoItemsFromDbMixin,
                                                ToDoAsJSONMixin,
                                                OrderedCategoriesMixin)
from bunch import Bunch
import shortuuid


import logging
logger = logging.getLogger('lawpal.services')


class ProjectCheckListService(UserFeedbackRequestMixin, ToDoItemsFromYamlMixin,
                              JavascriptRegionCloneMixin,
                              ToDoItemsFromDbMixin,
                              ToDoAsJSONMixin,
                              OrderedCategoriesMixin):
    """
    Provide a set of checklist items that are
    generated from the project transaction types
    """
    project = None
    checklist = []
    todos = []
    todos_by_cat = {}
    categories = []

    def __init__(self, project, **kwargs):
        self.project = project
        self.project_data = ProjectIntakeFormIsCompleteBunch(project=self.project)

        self.checklist = self.project.checklist()

        self.todos_by_cat, self.todos = self.get_todos()

        self.todos = self.append_todo_obj(self.todos)

        self.categories = self.get_categories()

        self.kwargs = kwargs

    def item_slug(self, item, **kwargs):
        """ the slug has to be consistent for each item, even when pulled from yaml file
        thus we cant use uuid here as it is generated unique every time; where as this is
        based on a uniqe combo of the item details"""
        name = self.project_data.slug(item_name=item.name)

        if len(kwargs.keys()) > 0:
            name = '{name}{extra}'.format(name=name, extra='-'.join([unicode(i) for i in kwargs.values()]))

        return shortuuid.uuid(name=name)

    def templatize(self, context, value):
        t = template.Template(value)
        return t.render(context)

    def item_context(self, item, **kwargs):
        c = template.Context(kwargs)

        # ensure we have a name and description
        item.name = item.name if hasattr(item, 'name') else None
        item.description = item.description if hasattr(item, 'description') else None

        # render the template with variables from the context
        if item.name is not None:
            item.name = unicode(self.templatize(context=c, value=item.name))

        if item.description is not None:
            item.description = unicode(self.templatize(context=c, value=item.description))

        return item

    def parse_checklist(self, current_length, checklist, **kwargs):
        for i, item in enumerate(checklist):
            # indicate attachment status
            try:
                item.num_attachments = len(item.attachment)
                item.has_attachment = item.num_attachments > 0
            except AttributeError:
                item.num_attachments = 0
                item.has_attachment = False
                item.attachment = []

            item.project = self.project
            item.slug = self.item_slug(item=item, i=i)
            item.description = item.description if hasattr(item, 'description') else None

            item.status = TODO_STATUS.new
            item.display_status = TODO_STATUS.get_desc_by_value(item.status)
            item.sort_position = current_length + i
            item.sort_position_by_cat = i
            item.item_hash_num = self.item_hash_num(item) # ties in with model.item_hash_num()
            # updated with various kwargs passed in
            item.update(kwargs)

    def item_hash_num(self, item):
        return '{primary}.{secondary}'.format(primary=int(item.get('sort_position', 0)), secondary=int(item.get('sort_position_by_cat', 0)))

    def navigation_items_object(self, slug):
        """
        Flatten the items by category and then get prev and next based on sorted cat
        """
        temp_todo_list = []
        navigation_items = Bunch(prev=None, current=None, next=None)

        for cat, items in self.todos_by_cat.iteritems():
            if items:
                for i in items:
                    temp_todo_list.append(i)

        for c, item in enumerate(temp_todo_list):

            try:
                previous = temp_todo_list[c-1]
            except IndexError:
                previous = None

            try:
                next = temp_todo_list[c+1]
            except IndexError:
                next = None

            if str(item.slug) == str(slug):
                navigation_items.prev = previous
                navigation_items.current = item
                navigation_items.next = next
                # exit the forloop
                break

        return navigation_items

    def process(self):
        logger.info('Process Project Checklist')
