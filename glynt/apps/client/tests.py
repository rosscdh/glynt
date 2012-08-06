"""
"""
from django.test import TestCase

from forms import SignupForm, AuthenticationForm


class SignupFormTest(TestCase):
    def setUp(self):
      self.form = SignupForm()

    def test_generate_username_from_email(self):
      """
      Tests generate_username_from_email returns a username max_length 30 
      from an email address
      """
      self.assertEqual(self.form.generate_username_from_email('userA@example.com'), 'useraexamplecom')
      self.assertEqual(self.form.generate_username_from_email('userAwithaverlonglonglonglongemailaddressfomrsomewhere@example.com'), 'userawithaverlonglonglonglonge')


class AuthenticationFormTest(TestCase):
    def setUp(self):
      self.form = AuthenticationForm()

    def test_username_field_accepts_email_and_displays_placeholder(self):
      """
      """
      self.assertTrue('placeholder' in self.form.fields['username'].widget.attrs)
      self.assertEqual(unicode(self.form.fields['username'].label), u'Email or Username')
      self.assertEqual(self.form.fields['username'].widget.attrs['placeholder'], 'username@example.com')