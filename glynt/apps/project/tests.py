"""
"""
from django.test import TestCase
from model_mommy import mommy

from glynt.apps.lawyer.models import Lawyer


class ProjectModelMethodsTest(TestCase):
    def setUp(self):
        lawyer = mommy.make('lawyer.Lawyer')
        self.project_with_lawyer = mommy.make('project.Project')
        self.project_lawyer = mommy.make('project.ProjectLawyer', project=self.project_with_lawyer, lawyer=lawyer)

        self.project_without_lawyer = mommy.make('project.Project')

    def test_get_primary_lawyer(self):
        """
        Test that we return a primary lawyer if present
        """
        self.assertNotEqual(None, self.project_with_lawyer.get_primary_lawyer())
        self.assertEqual(Lawyer, type(self.project_with_lawyer.get_primary_lawyer()))

    def test_not_get_primary_lawyer(self):
        """
        Test what we return when we have no lawyer for this project
        """
        self.assertEqual(None, self.project_without_lawyer.get_primary_lawyer())
        self.assertEqual(type(None), type(self.project_without_lawyer.get_primary_lawyer()))

    def test_has_lawyer(self):
        """
        Test the has lawyer facility works
        """
        self.assertEqual(True, self.project_with_lawyer.has_lawyer)
        self.assertEqual(False, self.project_without_lawyer.has_lawyer)
