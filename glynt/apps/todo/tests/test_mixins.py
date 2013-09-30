# -*- coding: utf-8 -*-
from django.test import TestCase

from glynt.apps.todo import TODO_STATUS

from model_mommy import mommy


class NumAttachmentsMixinText(TestCase):
    """
    Test the NumAttachmentsMixin ToDo object mixin
    which is responsible for getting setting and storing the 
    num_attachments value
    """

    def setUp(self):
        super(NumAttachmentsMixinText, self).setUp()

        self.project = mommy.make('project.Project')
        self.todo = mommy.make('todo.ToDo', status=TODO_STATUS.open, project=self.project, category='General')
        # self.attachment = mommy.make('todo.Attachment', project=self.project, todo=self.todo, uploaded_by=self.customer_user)


    def test_mixin_is_present(self):
        self.assertTrue(hasattr(self.todo, 'num_attachments'))
        self.assertTrue(hasattr(self.todo, 'num_attachments_plus'))
        self.assertTrue(hasattr(self.todo, 'num_attachments_minus'))

    def test_not_set_until_has_pk(self):
        todo = mommy.prepare('todo.ToDo', status=TODO_STATUS.open, project=self.project, category='General')
        self.assertEqual(None, todo.pk)
        self.assertEqual(0, todo.num_attachments)

    def test_num_attachments_sets_value_if_not_present(self):
        self.assertTrue('num_attachments' not in self.todo.data)

        # call the method
        self.todo.num_attachments

        # now we should have a value
        self.assertTrue('num_attachments' in self.todo.data)
        self.assertEqual(0, self.todo.data['num_attachments'])
        self.assertEqual(0, self.todo.num_attachments) # and the attrib

    def test_setter(self):
        self.assertEqual(0, self.todo.num_attachments)
        self.todo.num_attachments = 5
        self.assertEqual(5, self.todo.num_attachments)


    def test_incrementer(self):
        # event when we dont have it there by default
        self.assertTrue('num_attachments' not in self.todo.data)

        self.todo.num_attachments_plus()

        self.assertEqual(1, self.todo.data['num_attachments'])
        self.assertEqual(1, self.todo.num_attachments) # and the attrib

    def test_decrementer_not_less_than_0(self):
        # event when we dont have it there by default
        self.assertTrue('num_attachments' not in self.todo.data)

        self.todo.num_attachments_minus()

        self.assertTrue('num_attachments' not in self.todo.data) 
        self.assertEqual(0, self.todo.num_attachments)

    def test_decrementer(self):
        # event when we dont have it there by default
        self.assertTrue('num_attachments' not in self.todo.data)

        self.todo.num_attachments = 5
        self.todo.num_attachments_minus()

        self.assertEqual(4, self.todo.num_attachments)