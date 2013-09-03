# coding: utf-8
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization

AVAILABLE_FORMATS = ['json']


class BaseApiModelResource(ModelResource):
    """
    Base Resource that all other api resources extend
    used to apply our filters and specific rulesets
    """
    class Meta:
        serializer = Serializer(formats=AVAILABLE_FORMATS)
        authentication = SessionAuthentication()
        authorization = ReadOnlyAuthorization()
        include_resource_uri = False
        include_absolute_url = False
        always_return_data = True