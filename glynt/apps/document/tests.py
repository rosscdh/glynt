"""
Test the default app views
"""
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

from models import Document

public_urls = [
  reverse('document:view', kwargs={'slug': 'test-doc'}),
]

login_required_urls = [
  reverse('document:create'),
  reverse('document:edit', kwargs={'slug': 'test-doc'}),
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
    self.userA, is_new = User.objects.get_or_create(username='testA', password=password, email='testA@weareml.com')
    self.userB, is_new = User.objects.get_or_create(username='testB', password=password, email='testB@weareml.com')

    self.public_doc, is_new = Document.objects.get_or_create(owner=self.userA, name='Test Document', slug='test-doc', summary='This is a test doc', body='test', doc_status=Document.DOC_STATUS.active, is_public=True)
    self.private_doc, is_new = Document.objects.get_or_create(owner=self.userA, name='Private Test Document', slug='private-test-doc', summary='This is a private test doc', body='private test', doc_status=Document.DOC_STATUS.active, is_public=False)
    self.deleted_doc, is_new = Document.objects.get_or_create(owner=self.userA, name='Deleted Test Document', slug='deleted-test-doc', summary='This is a deleted test doc', body='deleted test', doc_status=Document.DOC_STATUS.deleted, is_public=True)
    self.draft_doc, is_new = Document.objects.get_or_create(owner=self.userA, name='Draft Test Document', slug='draft-test-doc', summary='This is a draft test doc', body='draft test', doc_status=Document.DOC_STATUS.draft, is_public=True)

  def check_response_token_helper(self,url,expected_status_code,expected_redirect_chain):
    """ Method to check response status code and redirect chain """
    response = self.client.get(url, follow=True)
    self.assertEqual(response.status_code, expected_status_code)
    self.assertEqual(response.redirect_chain, expected_redirect_chain)

  def test_anonymous_can_access_public_urls(self):
    for u in public_urls:
      self.check_response_token_helper(u, 200, [])

  def test_anonymous_cannot_access_logged_in_urls(self):
    for u in login_required_urls:
      self.check_response_token_helper(u, 404, [('http://testserver/accounts/login/?next=%s'%(u,), 302)])

  def test_anonymous_cannot_access_invalid_method_urls(self):
    """ Certain urls can only be post/put/patched to so test them """
    for u in invalid_method_urls:
      self.check_response_token_helper(u, 404, [('http://testserver/accounts/login/?next=%s'%(u,), 302)])

  def test_auth_user_cannot_access_invalid_method_urls(self):
    """ Certain urls can only be post/put/patched to so test them """
    user = self.client.login(username='testA', password='test')
    for u in invalid_method_urls:
      self.check_response_token_helper(u, 405, [])

  def test_anonymous_cannot_access_invalid_status_docs(self):
    for t in invalid_status_docs:
      u = reverse('document:view', kwargs={'slug': '%s-test-doc'%(t,)})
      self.check_response_token_helper(u, 404, [])

  def test_owner_can_access_restricted_status_docs(self):
    user = self.client.login(username='testA', password='test')
    for t in restricted_status_docs:
      u = reverse('document:view', kwargs={'slug': '%s-test-doc'%(t,)})
      self.check_response_token_helper(u, 200, [])

  def test_stranger_cant_access_restricted_status_docs(self):
    user = self.client.login(username='testB', password='test')
    for t in restricted_status_docs:
      u = reverse('document:view', kwargs={'slug': '%s-test-doc'%(t,)})
      self.check_response_token_helper(u, 404, [])

  def test_anonymous_cannot_access_private_doc(self):
    for t in restricted_status_docs:
      u = reverse('document:view', kwargs={'slug': '%s-test-doc'%(t,)})
      response = self.client.get(u, follow=True)
      self.assertEqual(response.status_code, 404)
      self.assertEqual(response.redirect_chain, [])

      

