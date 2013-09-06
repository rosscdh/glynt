# -*- coding: utf-8 -*-
"""
"""
from django.test import TestCase

from model_mommy import mommy
from glynt.apps.client.models import _get_or_create_user_profile

from glynt.apps.client.models import ClientProfile

#from .forms import SignupForm, AuthenticationForm


class ClientProfileCreateTest(TestCase):

  def setUp(self):
    self.subject = mommy.make('auth.User', username='subject', first_name='Test', last_name='Subject', email='subject+test@lawpal.com')

  def test__get_or_create_user_profile(self):
    result = _get_or_create_user_profile(self.subject)
    self.assertTrue(type(result) == tuple)

    profile, is_new = result

    self.assertTrue(type(profile) == ClientProfile)
    self.assertTrue(is_new == True)

  def test_profile_is_created_when_referenced(self):
    profile = self.subject.profile
    self.assertTrue(hasattr(self.subject, 'profile'))


# class SignupFormTest(TestCase):
#     def setUp(self):
#       self.form = SignupForm()

#     def test_generate_username_from_email(self):
#       """
#       Tests generate_username_from_email returns a username max_length 30 
#       from an email address
#       """
#       self.assertEqual(self.form.generate_username_from_email('userA@example.com'), 'useraexamplecom')
#       self.assertEqual(self.form.generate_username_from_email('userAwithaverlonglonglonglongemailaddressfomrsomewhere@example.com'), 'userawithaverlonglonglonglonge')


# class AuthenticationFormTest(TestCase):
#     def setUp(self):
#       self.form = AuthenticationForm()

#     def test_username_field_accepts_email_and_displays_placeholder(self):
#       """
#       """
#       self.assertTrue('placeholder' in self.form.fields['username'].widget.attrs)
#       self.assertEqual(unicode(self.form.fields['username'].label), u'Email or Username')
#       self.assertEqual(self.form.fields['username'].widget.attrs['placeholder'], 'username@example.com')