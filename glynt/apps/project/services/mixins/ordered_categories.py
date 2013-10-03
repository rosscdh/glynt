# -*- coding: UTF-8 -*-


class OrderedCategoriesMixin(object):
    """
    Mixin that provides access to a projects
    categories in an ordered fashion
    """
    project = None

    def category_initial(self):
        return ((c, c) for c in self.get_categories())

    def get_categories(self):
        if self.has_ordered_cats is not True:
            # return the set of category keys
            return self.todos_by_cat.keys()

        else:
            # return our ordered set
            return self.ordered_categories

    @property
    def has_ordered_cats(self):
        return type(self.project.data.get('category_order', False)) == list

    @property
    def ordered_categories(self):
        return self.project.data.get('category_order')