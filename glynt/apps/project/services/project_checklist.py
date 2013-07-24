# -*- coding: UTF-8 -*-
from collections import OrderedDict
from django import template
from django.template.defaultfilters import slugify


from glynt.apps.todo import TODO_STATUS
from glynt.apps.project.bunches import ProjectIntakeFormIsCompleteBunch

import logging
logger = logging.getLogger('lawpal.services')


class ProjectCheckListService(object):
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
        self.categories = self.get_categories()

    def slug(self, text):
        return slugify(text)

    # def todo_objects(self):
    #     self.project.todo_set.all()

    def get_todos(self):
        logger.info('Get Project transactions')
        checklist = []
        todos_by_cat = {}

        for c in self.checklist:
            if hasattr(c.todos, 'items'):
                for category, item in c.todos.items():
                    cat_slug = category
                    #cat_slug = self.slug(category)

                    if hasattr(item, 'repeater_key'):
                        repeater_key = item.repeater_key
                        singular = getattr(item, 'singular', None)

                        logger.info('Found repeater_key: %s' % repeater_key)

                        items = self.company_data.get(repeater_key, None)
                        num_items = 0

                        if not items and hasattr(self.company_data, repeater_key):
                            items = getattr(self.company_data, repeater_key)

                        if items:
                            # handle being passed a [] or (), otherwise it should be an int
                            if type(items) in [list]:
                                num_items = len(items)  
                            else:
                                num_items = int(items)
                                items = [i for i in xrange(1, num_items+1)]
                                logger.info('repeater_key: %s num_items %s' % (repeater_key, num_items,))

                        logger.info('All Items repeater_key: %s items: %s' % (repeater_key, items,))

                        if items:
                            # need to repeat this segment X times by
                            # field_name specified
                            cloned_checklist = list(item.checklist)  # clone the primary list

                            # merge lists
                            for i in items:
                                cloned_checklist = [self.item_context(item=cloned_item, full_name='{name} #{num}'.format(name=singular, num=i+1)) for i, cloned_item in enumerate(cloned_checklist)]
                                item.checklist = list(item.checklist + cloned_checklist)

                    # parse the list and assign extra attribs
                    self.parse_checklist(checklist=item.checklist)

                    checklist = list(checklist + item.checklist)

                    todos_by_cat[cat_slug] = todos_by_cat.get(cat_slug, [])
                    todos_by_cat[cat_slug] += item.checklist

        return  OrderedDict(sorted(todos_by_cat.items(), key=lambda t: t[0])), sorted(checklist)

    def item_context(self, item, **kwargs):
        t = template.Template(item.name)
        c = template.Context(kwargs)

        item.name = t.render(c)

        return item

    def parse_checklist(self, checklist):
        for item in checklist:
            # indicate attachment status
            try:
                item.num_attachements = len(item.attachment)
                item.has_attachment = item.num_attachements > 0
            except AttributeError:
                item.num_attachements = 0
                item.has_attachment = False
                item.attachment = []

            item.num_comments = 0
            item.status = TODO_STATUS.unassigned
            item.display_status = TODO_STATUS.get_desc_by_value(item.status)

    def get_categories(self):
        logger.info('Get Project transactions')
        cats = []
        for c in self.checklist:
            cats = list(set(cats + c.categories()))
        return sorted(cats)

    def process(self):
        logger.info('Process Project Checklist')
