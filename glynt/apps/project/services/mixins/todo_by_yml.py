# -*- coding: UTF-8 -*-
from collections import OrderedDict
import copy

from glynt.apps.project.services import logger


class ToDoItemsFromYamlMixin(object):
    """
    Mixin that provides extraction of todo checklist from
    The YAML Checklists
    """
    def get_yml_todos(self):
        """
        return the (cat, todos) tuple for create
        """
        checklist = []
        todos_by_cat = OrderedDict()

        logger.info('Get Project yml todo items and category')

        for c in self.checklist:

            if hasattr(c.todos, 'items'):

                for category, item in c.todos.items():

                    self.handle_repeater(item=item)
                    todos_by_cat[category] = []

                    if item.checklist:
                        # parse the list and assign extra attribs
                        self.parse_checklist(current_length=len(checklist), checklist=item.checklist, category=category)

                        todos_by_cat[category] = item.checklist
                        checklist = list(checklist + item.checklist)

        return  (todos_by_cat, checklist)

    def handle_repeater(self, item):
        repeater_key = None
        num_items = 0
        # does the item object contain a repeater_key
        if hasattr(item, 'repeater_key'):
            repeater_key = item.repeater_key
            # singular reference for verbage; i.e. Founder(<-singular value) #1
            singular = getattr(item, 'singular', None)

            logger.debug('Found repeater_key: %s' % repeater_key)

            # get the repeater_key values from the project_data
            items = self.project_data.get(repeater_key, None)

            # ok, we have no data form comapny_data based on the repeater_key
            # therefor we need to see if we can extract the data from an attribute/method
            # available on the project_data ProjectIntakeFormIsCompleteBunch object
            if not items and hasattr(self.project_data, repeater_key):
                items = getattr(self.project_data, repeater_key)

            # do we have items yet? great now we need to see if its a list
            # or an int, ie do we have a set of elements saved in the project_data
            # or is it a simple int value ie. num_officers which then allows us to generate
            if items:
                has_extra_dict = False
                # handle being passed a [] or (), otherwise it should be an int
                if type(items) in [dict]:
                    # if were pased a dict of repeater items
                    has_extra_dict = True
                    items = self.parse_repeater_dict(items=items)
                    num_items = len(items)
                    logger.debug('Created {num_items} from dict data'.format(num_items=num_items))

                elif type(items) in [list]:
                    num_items = len(items)
                    logger.debug('Created {num_items} from list data'.format(num_items=num_items))

                else:
                    # should be an int
                    num_items = int(items)
                    items = [i for i in xrange(1, num_items + 1)]
                    logger.debug('Created {num_items} from xrange'.format(num_items=num_items))

            logger.debug('All Items repeater_key: %s items: %s' % (repeater_key, items,))

            cloned_list = item.checklist[:]
            item.checklist = []

            if num_items > 0:
                # need to repeat this segment X times by
                # field_name specified

                for num in xrange(0, num_items):
                    # contextualize and replace the textual values
                    display_num = num + 1
                    logger.debug('Creating repeater {repeater_key}, {num}/{display_num}'.format(repeater_key=repeater_key, num=num, display_num=display_num))

                    # set the extra dict to be passed in if it exists
                    extra = items[num] if has_extra_dict is True else {}

                    # append to the item.checklist
                    # account for the extra dict which could contain region-clone key->vals
                    generic_name = '{name} #{num}'.format(name=singular,
                                                          num=display_num)

                    # update the yml line items with the context provided here
                    # by the kwargs
                    item.checklist += [self.item_context(item=copy.deepcopy(cloned_item),
                                                        num=display_num,
                                                        generic_name=generic_name,
                                                        **extra) for cloned_item in cloned_list]
