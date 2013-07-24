# -*- coding: UTF-8 -*-
from collections import OrderedDict
from django.template.defaultfilters import slugify

from glynt.apps.todo import TODO_STATUS

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
        self.company_data = self.project.company.data

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
            for category, item in c.todos.items():

                cat_slug = category
                #cat_slug = self.slug(category)

                todos_by_cat[cat_slug] = todos_by_cat.get(cat_slug, [])
                todos_by_cat[cat_slug] += item.checklist

                if hasattr(item, 'repeater_key'):
                    repeater_key = item.repeater_key
                    print repeater_key
                    items = self.company_data.get(repeater_key, None)
                    if items:
                        pass
                    # need to repeat this segment X times by
                    # field_name specified

                # parse the list and assign extra attribs
                self.parse_checklist(checklist=item.checklist)

                checklist += item.checklist

        return  OrderedDict(sorted(todos_by_cat.items(), key=lambda t: t[0])), sorted(checklist)

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
