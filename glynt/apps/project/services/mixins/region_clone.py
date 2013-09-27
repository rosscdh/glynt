# -*- coding: UTF-8 -*-
import re

from glynt.apps.project.services import logger


RE_FIND_END_NUMERAL = re.compile(r'_(\d+)$')


class JavascriptRegionCloneMixin(object):
    """
    A mixin to ensure that we can extract the javascript generated
    cloneable-region values
    """
    def extract_repeater_values(self, items):
        cleaned_items = []
        if items is None:
            logger.error('items passed into JavascriptRegionCloneMixin is None')
        else:
            for key, item_value in sorted(items.items()):
                id = item_value.get('id')
                val = item_value.get('val')

                match = RE_FIND_END_NUMERAL.search(key)
                if match is None:
                    # this is the primary first item (as it has no *_<int>)
                    index = 0
                else:
                    # these are secondary items (as they have *_<int>)
                    # remove the _ and convert to integer
                    index = int(match.group().replace('_', ''))

                # remove the _<int> from the id
                # if it exists
                match = RE_FIND_END_NUMERAL.search(id)
                if match is not None:
                    id = key.replace(match.group(), '')

                logger.debug('\n{index} - {id}: {val}\n\n'.format(index=index,
                                                                  id=id,
                                                                  val=val))

                try:
                    obj = cleaned_items[index]
                    obj[id] = val
                    cleaned_items[index] = obj
                    logger.debug("updated new item {obj}\n".format(obj=obj))
                except IndexError:
                    obj = {}
                    obj[id] = val
                    cleaned_items.insert(index, obj)
                    logger.debug("inserted new item {obj}\n".format(obj=obj))

                logger.debug("cleaned_items: {cleaned_items}\n".format(cleaned_items=cleaned_items))

        return cleaned_items

    def parse_repeater_dict(self, items):
        return self.extract_repeater_values(items)
