# -*- coding: UTF-8 -*-
from django.template.defaultfilters import slugify

from collections import OrderedDict
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
        self.checklist = self.project.checklist()
        self.todos_by_cat, self.todos = self.get_todos()

        self.categories = self.get_categories()

    def slug(self, text):
        return slugify(text)

    def get_todos(self):
        logger.info('Get Project transactions')
        checklist = []
        todos_by_cat = {}

        for c in self.checklist:
            for category, item in c.todos.items():

                cat_slug = category
                #cat_slug = self.slug(category)

                todos_by_cat[cat_slug] = todos_by_cat.get(cat_slug, [])
                todos_by_cat[cat_slug] = item.checklist

                if item.type == 'repeater':
                    # need to repeat this segment X times by
                    # field_name specified
                    pass

                checklist += item.checklist

        return  OrderedDict(sorted(todos_by_cat.items(), key=lambda t: t[0])), sorted(checklist)

    def get_categories(self):
        logger.info('Get Project transactions')
        cats = []
        for c in self.checklist:
            cats += c.categories()
        return sorted(cats)

    def process(self):
        logger.info('Process Project Checklist')
