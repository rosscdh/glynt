# -*- coding: UTF-8 -*-
from django.test import TestCase

from threadedcomments.models import ThreadedComment


class ThreadedCommentsTest(TestCase):
    """
    Test we have patched in the django-rulez
    the can_read can_edit and can_delete
    methods are patched in in default/models.py
    and are used in the v2 api to test that the current user
    can access the threaded comment
    """
    def setUp(self):
        self.subject = ThreadedComment

    def test_as_can_read(self):
        self.assertTrue(hasattr(self.subject, 'can_read'))

    def test_as_can_edit(self):
        self.assertTrue(hasattr(self.subject, 'can_edit'))

    def test_as_can_delete(self):
        self.assertTrue(hasattr(self.subject, 'can_delete'))
