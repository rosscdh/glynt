# -*- coding: UTF-8 -*-
from django.test import TestCase
from taggit.managers import TaggableManager
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

    def test_has_tags_manager(self):
        self.assertTrue(hasattr(self.subject, 'tags'))
        self.assertEqual('_TaggableManager', self.subject.tags.__class__.__name__)

    def test_has_absolute_deeplink_url(self):
        self.assertTrue(hasattr(self.subject, 'absolute_deeplink_url'))
