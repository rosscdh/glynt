# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet

from glynt.casper import BaseLawyerCustomerProjectCaseMixin


class CustomerModelTest(BaseLawyerCustomerProjectCaseMixin):
    def test_get_absolute_url(self):
        self.assertEqual('/customers/customer/', self.customer.get_absolute_url())

    def test_full_name(self):
        self.assertEqual(u' ', self.customer.full_name)

    def test_profile_photo(self):
        self.assertEqual('/static/img/default_avatar.png', self.customer.profile_photo)

    def test_phone(self):
        self.assertEqual('', self.customer.phone)

    def test_companies(self):
        self.assertEqual(QuerySet, type(self.customer.companies))
        self.assertEqual(1, len(self.customer.companies))

    def test_primary_company(self):
        self.assertEqual(self.company, self.customer.primary_company)


class CustomerProfileSetupFormTest(BaseLawyerCustomerProjectCaseMixin):
    def test(self):
        url = reverse('customer:setup_profile')

        # User not logged in
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/?next=/customers/setup/')

        self.client.login(username=self.customer_user.username, password=self.password)

        # Valid user
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # Valid submission
        response = self.client.post(url, {
            'first_name': 'Joe',
            'last_name': 'Bloggs',
            'email': 'joe@example.com',
            'phone': '123123123',
            'company_name': 'Startup, Inc',
        }, follow=True)

        redirect = reverse('dashboard:overview')
        self.assertRedirects(response, redirect)
