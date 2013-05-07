import factory

from django.contrib.sites.models import Site
from django.contrib.auth.models import User, AnonymousUser

from glynt.apps.document.models import ClientCreatedDocument, DocumentTemplate, DocumentHTML
from glynt.apps.sign.models import DocumentSignature

import random


class SiteFactory(factory.Factory):
    FACTORY_FOR = Site
    domain = factory.LazyAttributeSequence(lambda a, n: 'http://www.example-{0}.com'.format(n))
    name = factory.LazyAttributeSequence(lambda a, n: 'Test Domain Example {0}'.format(n))


class LoggedOutUserFactory(factory.Factory):
    FACTORY_FOR = AnonymousUser


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    first_name = 'Test'
    last_name = 'User'
    is_superuser = False
    username = factory.LazyAttributeSequence(lambda a, n: '{0}_{1}'.format(a.first_name, n).lower())
    email = factory.LazyAttributeSequence(lambda a, n: '{0}.{1}+{2}@lawpal.com'.format(a.first_name, a.last_name, n).lower())
    password = 'test'


class AdminFactory(UserFactory):
    is_superuser = True


class TemplateFactory(factory.Factory):
    FACTORY_FOR = DocumentTemplate
    owner = factory.SubFactory(UserFactory)
    body = u'<p>body</p>'


class DocumentFactory(factory.Factory):
    FACTORY_FOR = ClientCreatedDocument
    name = factory.LazyAttributeSequence(lambda a, n: 'Document_{0}'.format(n))
    owner = factory.SubFactory(UserFactory)
    source_document = factory.SubFactory(TemplateFactory)
    doc_data = {'username':'test username', 'title': 'Title'}
    body = u'<p>body</p>'


class DocumentHTMLFactory(factory.Factory):
    FACTORY_FOR = DocumentHTML
    document = factory.SubFactory(DocumentFactory)


class SignatureFactory(factory.Factory):
    FACTORY_FOR = DocumentSignature
    document = factory.SubFactory(DocumentFactory)
    user = factory.SubFactory(UserFactory)
    key_hash = factory.LazyAttributeSequence(lambda a, n: 'r3n{0}0m'.format(n))
