import factory

from django.contrib.auth.models import User
from glynt.apps.document.models import ClientCreatedDocument, DocumentTemplate, DocumentHTML


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    first_name = 'Test'
    last_name = 'User'
    is_superuser = False
    username = factory.LazyAttributeSequence(lambda a, n: '{0}_{1}'.format(a.first_name, n).lower())
    email = factory.LazyAttributeSequence(lambda a, n: '{0}.{1}+{2}@lawpal.com'.format(a.first_name, a.last_name, n).lower())


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