# -*- coding: UTF-8 -*-
from bunch import Bunch
from collections import OrderedDict

from glynt.apps.todo.models import ToDo
from glynt.apps.project.services import logger


class ToDoItemsFromDbMixin(object):
    slugs = None
    _db_todos_list = None

    def get_db_todos(self):
        """
        return the (cat, todos) tuple for create
        """
        checklist = []
        todos_by_cat = OrderedDict()

        logger.info('Get Project db todo items and category')

        for todo in self.db_todos():
            checklist.append(todo)

            if todo.category not in todos_by_cat:
                todos_by_cat[todo.category] = []

            todos_by_cat[todo.category].append(todo)

        return (todos_by_cat, checklist)

    def db_todos(self):
        if self._db_todos_list is None:
            self._db_todos_list = self.project.todo_set.all().select_related()

        return self._db_todos_list

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

            if db_item.is_deleted is True and db_item.slug in slugs:
                del slugs[db_item.slug]
                self.delete_item(db_item)
                logger.debug('Deleted the todolist slug: {slug}'.format(slug=db_item.slug))
            else:

                try:
                    # index exists so we have them already so append this key
                    slugs[db_item.slug].obj = db_item
                    self.modify_item_values(slugs[db_item.slug])
                except KeyError:
                    # if the index does not exist, it means its
                    # a custom created item that the user has added
                    slugs[db_item.slug] = db_item
                    slugs[db_item.slug].obj = db_item

                    self.todos_by_cat[db_item.category] = \
                        self.todos_by_cat.get(db_item.category, [])

                    self.todos_by_cat[db_item.category].append(slugs[db_item.slug])

        # return the actual items and not our temp dictionary
        return slugs.values()

    def modify_item_values(self, item):
        item.__dict__.update(item.obj.__dict__)
        logger.debug('checklist item status: {name} (display_status)'.format(name=item.name.encode('utf-8'), display_status=item.display_status))

    def todo_data_defaults(self, todo):
        """
        append requried data attribs and values to a todo object
        before being used in bulk_create
        """
        todo.data['num_attachments'] = 0
        return todo

    def bulk_create(self):
        logger.debug('start bulk_create')

        todo_list = []
        db_todo_slugs = [t.slug for t in self.db_todos()]

        for t in self.todos:
            if type(t) == Bunch and hasattr(t, 'toDict'):
                t = t.toDict()
                t.pop('attachment', None)
                t.pop('has_attachment', None)
                t.pop('num_attachments', None)
                t.pop('group', None)
                t.pop('note', None)
                if t.get('slug') is not None and t.get('slug') not in db_todo_slugs:

                    todo = self.todo_data_defaults(ToDo(**t))

                    todo_list.append(todo)

        if todo_list:
            ToDo.objects.bulk_create(todo_list)
