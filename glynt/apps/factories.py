# -*- coding: utf-8 -*-
import factory

from django.contrib.sites.models import Site
from django.contrib.auth.models import User, AnonymousUser


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
