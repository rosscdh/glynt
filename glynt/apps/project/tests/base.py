# -*- coding: UTF-8 -*-
"""
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from model_mommy import mommy

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin

from glynt.apps.lawyer.models import Lawyer
from glynt.apps.project.models import Project
from glynt.apps.project import PROJECT_STATUS, PROJECT_LAWYER_STATUS

import itertools
import os


class EnsureProjectsAreAvailableInContextOnAllPagesTest(BaseLawyerCustomerProjectCaseMixin):
    """
    Test a random set of urls for the presence of the projects and projects objects
    """
    def setUp(self):
        super(EnsureProjectsAreAvailableInContextOnAllPagesTest, self).setUp()

        self.urls = [
                        reverse('public:why-lawpal'),
                        reverse('public:for-lawyers'),
                        reverse('public:terms'),
                        reverse('public:about'),
                    ]

        #self.auth_urls = self.urls + [
        self.auth_urls = [
            reverse('dashboard:overview'),
            reverse('dashboard:checklist', kwargs={'uuid': self.project.uuid}),
            reverse('dashboard:project', kwargs={'uuid': self.project.uuid}),
        ]

    def test_projects_are_never_available_to_unauthorised_users(self):
        for u in self.urls:
            resp = self.client.get(u)
            request = resp.context['request']

            self.assertTrue(hasattr(request, 'project'))
            self.assertTrue(request.project is None)
            
            self.assertTrue(type(request.projects) is list)
            self.assertEqual(len(request.projects), 0)

    def test_projects_are_always_available_to_lawyer_user(self):
        """
        The Dashboard url for the LAWYER does not contain project info
        It is a list of projects associated with the lawyer in question
        """
        self.client.login(username=self.lawyer_user.username, password=self.password)

        for u in self.auth_urls:
            resp = self.client.get(u)
            request = resp.context['request']

            self.assertTrue(hasattr(request, 'project'))
            self.assertTrue(type(request.project) == Project)

            self.assertTrue(hasattr(request, 'projects'))
            self.assertTrue(type(request.projects) is list)
            self.assertEqual(len(request.projects), 1)

    def test_projects_are_always_available_customer(self):
        """
        """
        self.client.login(username=self.customer_user.username, password=self.password)

        for u in self.auth_urls:
            resp = self.client.get(u)
            request = resp.context['request']

            self.assertTrue(hasattr(request, 'project'))
            self.assertTrue(type(request.project) == Project)

            self.assertTrue(hasattr(request, 'projects'))
            self.assertTrue(type(request.projects) is QuerySet)
            self.assertEqual(len(request.projects), 1)


class ProjectModelMethodsTest(TestCase):
    """
    Test the project model methods
    """
    def setUp(self):
        self.user = mommy.make('auth.User')
        self.company = mommy.make('company.Company', customers=[self.user])
        self.lawyer = mommy.make('lawyer.Lawyer')
        self.project_with_lawyer = mommy.make('project.Project', company=self.company)

        mommy.make('project.ProjectLawyer', project=self.project_with_lawyer, lawyer=self.lawyer, status=PROJECT_LAWYER_STATUS.assigned)

        self.project_without_lawyer = mommy.make('project.Project', company=self.company)

    def test_project_status(self):
        """ Test the Display name is the same as the named_tuple description"""
        self.assertEqual(self.project_with_lawyer.display_status, PROJECT_STATUS.get_desc_by_value(self.project_with_lawyer.status))
        self.assertEqual(self.project_with_lawyer.display_status, 'New')
        self.assertEqual(self.project_with_lawyer.is_new, True)
        self.assertEqual(self.project_with_lawyer.is_open, False)
        self.assertEqual(self.project_with_lawyer.is_closed, False)

    def test_transaction_types(self):
        """ returns a list of the type of transaction associated with this project """
        self.assertEqual(type(self.project_with_lawyer.transaction_types), list)

    def test_get_primary_lawyer_not_present(self):
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

    def test_get_primary_lawyer_present(self):
        self.assertTrue(self.project_with_lawyer.get_primary_lawyer() is not None)
        self.assertEqual(type(self.project_with_lawyer.get_primary_lawyer()), Lawyer)

        # projects without a lawyer return none for this method
        self.assertTrue(self.project_without_lawyer.get_primary_lawyer() is None)
        self.assertEqual(type(self.project_without_lawyer.get_primary_lawyer()), type(None))

    def test_notification_recipients(self):
        self.assertEqual(type(self.project_with_lawyer.notification_recipients()), QuerySet)
        # there should be 2 recipients here.. the customer and the 1 assigned lawyer
        self.assertEqual(len(list(self.project_with_lawyer.notification_recipients())), 2)

        self.assertEqual(type(self.project_without_lawyer.notification_recipients()), QuerySet)
        # there should be 1 recipients here.. jsut the customer as we have no lawyers
        self.assertEqual(len(list(self.project_without_lawyer.notification_recipients())), 1)

    """ Removed until project status change requirements comes up """
    # def test_project_status_to_open(self):
    #     self.project_with_lawyer.open(self.user)
    #     self.assertEqual(self.project_with_lawyer.is_open, False)


class ContactUsModalTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
    test_path = os.path.dirname(__file__)

    def test_contact_us_modal_js(self):
        self.client.login(username=self.customer_user.username, password=self.password)

        url = reverse('project:create')
        self.assertTrue(self.load_casper_file(js_file='contact-us-modal.js', test_label='Test the Contact Us modal', url=url))
