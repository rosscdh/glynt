# -*- coding: UTF-8 -*-
from django.test import TestCase
from model_mommy import mommy
import mock


from glynt.apps.transact.models import Transaction
from glynt.apps.project.mixins import ProjectCategoriesMixin
from glynt.apps.project.models import Project


class ProjectCategoriesMixinTest(TestCase):
    """
    Test for the Mixin that handles categories
    stored in the project.data JSON field
    """
    fixtures = ['transact.json']

    def setUp(self):
        self.project = mommy.make('project.Project', transactions=(Transaction.objects.get(slug='CS'), Transaction.objects.get(slug='SF'),))
        self.todo =  mommy.make('todo.Todo', project=self.project, category='Delete Me Category')

    def test_categories_mixin_present(self):
        self.assertTrue(issubclass(Project, ProjectCategoriesMixin))  # inherits the mixin

        self.assertTrue(hasattr(self.project, 'categories'))
        self.assertTrue(hasattr(self.project, 'original_categories'))
        self.assertTrue(hasattr(self.project, 'delete_categories'))
        self.assertTrue(hasattr(self.project, 'delete_items_by_category'))

    def test_categories(self):
        # ensure that the category_order key has not yet been set
        self.assertTrue(self.project.data.get('category_order', False) is False)

        # call project.categories which then should return the standard todo set (because we have not yet ordered the cats)
        self.assertEqual([self.todo.category], self.project.categories)

    def test_categories_setter(self):
        new_category = u'A Monkey came along Category'

        # make a copy
        current_categories = self.project.categories
        # append
        current_categories.append(new_category)

        # set the project categories
        # this is the subject of the test the categories.setter
        self.project.categories = current_categories
        self.project.save(update_fields=['data'])

        # test we now have this new category in the list.. even tho there are
        # no todo items associated with it
        self.assertEqual([self.todo.category, new_category], self.project.categories)

    @mock.patch.object(ProjectCategoriesMixin, 'original_categories')
    def test_original_categories(self, mock_method):
        # ensure that the category_order key has not yet been set
        self.assertTrue(self.project.data.get('category_order', False) is False)

        # call the mocked method
        self.project.categories

        # is called when no local categories are provided
        mock_method.assert_called_once()

    def test_delete_categories(self):
        """
        removes the actual category as well as
        sets the related todo.is_deleted = True
        value
        """
        new_category = u'A Monkey came along Category'
        # make a copy
        current_categories = self.project.categories
        # append
        current_categories.append(new_category)

        # set the project categories
        # this is the subject of the test the categories.setter
        self.project.categories = current_categories
        self.project.save(update_fields=['data'])

        new_todo = mommy.make('todo.Todo', project=self.project, category=new_category)
        # ensure that the related todo in this category is set to is_deleted=False
        self.assertFalse(new_todo.is_deleted is True)

        # as expected?
        self.assertEqual([self.todo.category, new_category], self.project.categories)

        self.project.delete_categories(delete_categories=new_category)
        self.project.save(update_fields=['data'])

        # now we have only the original category
        self.assertEqual([self.todo.category], self.project.categories)
        # ensure that the related todo in this category is set to is_deleted=True
        self.assertTrue(self.project.todo_set.get(pk=new_todo.pk).is_deleted)

    def test_delete_items_by_category(self):
        new_category = u'A Monkey came along Category'

        new_todo = mommy.make('todo.Todo', project=self.project, category=new_category)
        # ensure that the related todo in this category is set to is_deleted=False
        self.assertFalse(new_todo.is_deleted is True)

        self.project.delete_items_by_category(delete_categories=new_category)
        self.project.save(update_fields=['data'])

        # ensure that the related todo in this category is set to is_deleted=True
        self.assertTrue(self.project.todo_set.get(pk=new_todo.pk).is_deleted)
