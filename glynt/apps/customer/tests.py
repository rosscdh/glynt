# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from glynt.casper import BaseLawyerCustomerProjectCaseMixin, PyQueryMixin


class CustomerProfileSetupFormTest(BaseLawyerCustomerProjectCaseMixin, PyQueryMixin):
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
