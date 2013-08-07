# -*- coding: UTF-8 -*-
from django import template

from glynt.apps.todo import TODO_STATUS
from glynt.apps.project.bunches import ProjectIntakeFormIsCompleteBunch

from bunch import Bunch

import copy
from collections import OrderedDict
import hashlib
import json
import logging
logger = logging.getLogger('lawpal.services')


class ToDoItemsFromYamlMixin(object):
    """
    Mixin that provides extraction of todo checklist from
    The YAML Checklists
    """
    def get_todos(self):
        logger.info('Get Project transactions')
        checklist = []
        todos_by_cat = {}

        for c in self.checklist:
            if hasattr(c.todos, 'items'):
                for category, item in c.todos.items():
                    cat_slug = category

                    self.handle_repeater(item=item)

                    if not item.checklist:
                        # no repeater items found or empty category
                        todos_by_cat[cat_slug] = []
                    else:
                        # parse the list and assign extra attribs
                        self.parse_checklist(checklist=item.checklist, category=category)
                        checklist = list(checklist + item.checklist)

                        todos_by_cat[cat_slug] = todos_by_cat.get(cat_slug, [])
                        todos_by_cat[cat_slug] += item.checklist

        return  OrderedDict(sorted(todos_by_cat.items(), key=lambda t: t[0])), sorted(checklist)

    def handle_repeater(self, item):
        repeater_key = None
        num_items = 0
        # does the item object contain a repeater_key
        if hasattr(item, 'repeater_key'):
            repeater_key = item.repeater_key
            # singular reference for verbage; i.e. Founder(<-singular value) #1
            singular = getattr(item, 'singular', None)

            logger.info('Found repeater_key: %s' % repeater_key)

            # get the repeater_key values from the company data
            items = self.company_data.get(repeater_key, None)

            # ok, we have no data form comapny_data based on the repeater_key
            # therefor we need to see if we can extract the data from an attribute/method
            # available on the company_data ProjectIntakeFormIsCompleteBunch object
            if not items and hasattr(self.company_data, repeater_key):
                items = getattr(self.company_data, repeater_key)

            # do we have items yet? great now we need to see if its a list
            # or an int, ie do we have a set of elements saved in the company_data
            # or is it a simple int value ie. num_officers which then allows us to generate
            if items:
                # handle being passed a [] or (), otherwise it should be an int
                if type(items) in [list]:
                    num_items = len(items)
                    logger.info('Created num_items from data key')
                else:
                    # should be an int
                    num_items = int(items)
                    items = [i for i in xrange(1, num_items+1)]
                    logger.info('Created num_items from xrange')

            logger.info('All Items repeater_key: %s items: %s' % (repeater_key, items,))

            cloned_list = item.checklist[:]
            item.checklist = []

            if num_items > 0:
                # need to repeat this segment X times by
                # field_name specified
                for num in xrange(1, num_items+1):
                    # contextualize and replace teh textual values
                    item.checklist += [self.item_context(item=copy.deepcopy(cloned_item), full_name='{name} #{num}'.format(name=singular, num=num)) for cloned_item in cloned_list]

    def item_context(self, item, **kwargs):
        c = template.Context(kwargs)

        # ensure we have a name and description
        item.name = item.name if hasattr(item, 'name') else None
        item.description = item.description if hasattr(item, 'description') else None

        # render the template with variables from the context
        item.name = self.templateize(context=c, value=item.name)
        item.description = self.templateize(context=c, value=item.description)

        return item


class ToDoItemsFromDbMixin(object):
    slugs = None
    db_todos_list = None

    def db_todos(self):
        if self.db_todos_list is None:
            self.db_todos_list = self.project.todo_set.filter(project=self.project)
        return self.db_todos_list

    def todos_by_slug(self, todos):
        if self.slugs is None:
            self.slugs = {}
            for item in todos:
                self.slugs[item.slug] = item
        return self.slugs

    def delete_item(self, item):
        for cat, items in self.todos_by_cat.iteritems():
            for c, i in enumerate(items):
                if item.slug == i.slug:
                    del items[c]
                    break


    def append_todo_obj(self, todos):
        """ Append obj to the todo item """
        slugs = self.todos_by_slug(todos)
        # get a set of todo items in the database
        # and append them to the item object
        for db_item in self.db_todos():
            if db_item.is_deleted is True:
                del slugs[db_item.slug]
                self.delete_item(db_item)
            else:
                try:
                    slugs[db_item.slug].obj = db_item
                    self.modify_item_values(slugs[db_item.slug])
                except KeyError:
                    # if the index does not exist, it means its 
                    # a custom created item that the user has added
                    slugs[db_item.slug] = db_item
                    slugs[db_item.slug].obj = db_item
                    self.todos_by_cat[db_item.category] = self.todos_by_cat.get(db_item.category, [])
                    self.todos_by_cat[db_item.category].append(slugs[db_item.slug])

        # return the actual items and not our temp dictionary
        return slugs.values()

    def modify_item_values(self, item):
        item.__dict__.update(item.obj.__dict__)
        logger.debug('checklist item status: %s %s' % (item.name, item.display_status,))


class ProjectCheckListService(ToDoItemsFromYamlMixin, ToDoItemsFromDbMixin):
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
        self.company_data = ProjectIntakeFormIsCompleteBunch(project=self.project)

        self.checklist = self.project.checklist()
        self.todos_by_cat, self.todos = self.get_todos()
        self.todos = self.append_todo_obj(self.todos)
        self.categories = self.get_categories()
        self.kwargs = kwargs

    def item_slug(self, item, **kwargs):
        """ the slug has to be consistent for each item, even when pulled from yaml file
        thus we cant use uuid here as it is generated unique every time; where as this is
        based on a uniqe combo of the item details"""
        m = hashlib.sha1()
        m.update(self.company_data.slug(item_name=item.name))
        if len(kwargs.keys()) > 0:
            m.update(json.dumps(kwargs))
        return m.hexdigest()

    def templateize(self, context, value):
        t = template.Template(value)
        return t.render(context)

    def parse_checklist(self, checklist, **kwargs):
        for i, item in enumerate(checklist):
            # indicate attachment status
            try:
                item.num_attachments = len(item.attachment)
                item.has_attachment = item.num_attachments > 0
            except AttributeError:
                item.num_attachments = 0
                item.has_attachment = False
                item.attachment = []

            item.slug = self.item_slug(item=item, i=i)
            item.description = item.description if hasattr(item, 'description') else None
            item.num_comments = 0
            item.status = TODO_STATUS.new
            item.display_status = TODO_STATUS.get_desc_by_value(item.status)
            # updated with various kwargs passed in
            item.update(kwargs)

    def get_categories(self):
        logger.info('Get Project transactions')
        cats = []
        for c in self.checklist:
            cats = list(set(cats + c.categories()))
        return sorted(cats)

    def category_initial(self):
        return ((c, c) for c in self.get_categories())

    def navigation_items_object(self, slug):
        """ flatten the items by category and then get prev and next based on sorted cat"""
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

            logger.debug('slug: {slug} == {item_slug} type: {type} == {type_b}'.format(slug=item.slug, item_slug=slug, type=type(str(item.slug)), type_b=type(str(slug))))

            if str(item.slug) == str(slug):
                navigation_items.prev = previous
                navigation_items.current = item
                navigation_items.next = next
                # exit the forloop
                break

        return navigation_items

    def process(self):
        logger.info('Process Project Checklist')
