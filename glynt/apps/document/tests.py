"""
Test the default app views
"""
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from glynt.apps.document.models import Document
from glynt.apps.flyform.models import FlyForm
from glynt.apps.flyform.tests import BASE_JSON

public_urls = [
  reverse('document:view', kwargs={'slug': 'test-doc'}),
]

login_required_urls = [
    reverse('document:my_delete', kwargs={'pk': 1}),
    reverse('document:my_undelete', kwargs={'pk': 1}),
    reverse('document:my_clone', kwargs={'pk': 1}),
    reverse('document:my_persist', kwargs={'pk': 1}),
    reverse('document:my_review', kwargs={'slug': 'test-doc'}),
    reverse('document:my_view', kwargs={'slug': 'test-doc'}),
    reverse('document:author_doc'),
    reverse('document:export', kwargs={'slug': 'test-doc'}),
    reverse('document:validate_form', kwargs={'slug': 'test-doc'}),
]

invalid_method_urls = [
  reverse('document:export', kwargs={'slug': 'test-doc'}),
]

invalid_status_docs = ['deleted', 'draft']
restricted_status_docs = ['private','draft']

class DocumentTest(TestCase):
  def setUp(self):
    self.client = Client()

    password = make_password('test')
    self.user_a, is_new = User.objects.get_or_create(username='test_a', password=password, email='test_a@weareml.com')
    self.user_b, is_new = User.objects.get_or_create(username='test_b', password=password, email='test_b@weareml.com')

    self.public_doc, is_new = Document.objects.get_or_create(owner=self.user_a, name='Test Document', slug='test-doc', summary='This is a test doc', body='test', doc_status=Document.DOC_STATUS.active, is_public=True, flyform=FlyForm.objects.create(body=[BASE_JSON]))
    self.private_doc, is_new = Document.objects.get_or_create(owner=self.user_a, name='Private Test Document', slug='private-test-doc', summary='This is a private test doc', body='private test', doc_status=Document.DOC_STATUS.active, is_public=False, flyform=FlyForm.objects.create(body=[BASE_JSON]))
    self.deleted_doc, is_new = Document.objects.get_or_create(owner=self.user_a, name='Deleted Test Document', slug='deleted-test-doc', summary='This is a deleted test doc', body='deleted test', doc_status=Document.DOC_STATUS.deleted, is_public=True, flyform=FlyForm.objects.create(body=[BASE_JSON]))
    self.draft_doc, is_new = Document.objects.get_or_create(owner=self.user_a, name='Draft Test Document', slug='draft-test-doc', summary='This is a draft test doc', body='draft test', doc_status=Document.DOC_STATUS.draft, is_public=True, flyform=FlyForm.objects.create(body=[BASE_JSON]))

  def check_response_token_helper(self, url, expected_status_code, expected_redirect_chain):
    """ Method to check response status code and redirect chain """
    response = self.client.get(url, follow=True)

    if response.status_code != expected_status_code:
        print "\n"
        print url
        print "%s %s" % (response.status_code, expected_status_code,)
        print "\n"
    self.assertEqual(response.status_code, expected_status_code)
    self.assertEqual(response.redirect_chain, expected_redirect_chain)

  def test_anonymous_can_access_public_urls(self):
    for url in public_urls:
      self.check_response_token_helper(url, 200, [])

  def test_anonymous_cannot_access_logged_in_urls(self):
    """ status 200 as the system redirects """
    self.client.logout()
    for url in login_required_urls:
      self.check_response_token_helper(url, 200, [('http://testserver/client/login/?next=%s'%(url, ), 302)])

  def test_anonymous_cannot_access_invalid_method_urls(self):
    """ Certain urls can only be post/put/patched to so test them """
    self.client.logout()
    for url in invalid_method_urls:
      self.check_response_token_helper(url, 200, [('http://testserver/client/login/?next=%s'%(url, ), 302)])

  def test_auth_user_cannot_access_invalid_method_urls(self):
    """ Certain urls can only be post/put/patched to so test them """
    user = self.client.login(username='test_a', password='test')
    for url in invalid_method_urls:
      self.check_response_token_helper(url, 404, [])

  def test_anonymous_cannot_access_invalid_status_docs(self):
    for name in invalid_status_docs:
      url = reverse('document:view', kwargs={'slug': '%s-test-doc'%(name, )})
      self.check_response_token_helper(url, 404, [])

  def test_owner_can_access_restricted_status_docs(self):
    user = self.client.login(username='test_a', password='test')
    for name in restricted_status_docs:
      url = reverse('document:view', kwargs={'slug': '%s-test-doc'%(name, )})
      self.check_response_token_helper(url, 200, [])

  def test_stranger_cant_access_restricted_status_docs(self):
    user = self.client.login(username='test_b', password='test')
    for name in restricted_status_docs:
      url = reverse('document:view', kwargs={'slug': '%s-test-doc'%(name, )})
      self.check_response_token_helper(url, 404, [])

  def test_anonymous_cannot_access_private_doc(self):
    for name in restricted_status_docs:
      url = reverse('document:view', kwargs={'slug': '%s-test-doc'%(name, )})
      response = self.client.get(url, follow=True)
      self.assertEqual(response.status_code, 404)
      self.assertEqual(response.redirect_chain, [])

      

