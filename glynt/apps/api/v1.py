from django.conf.urls.defaults import url
from django.utils import simplejson as json
import ast

from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from tastypie.api import Api
from tastypie.serializers import Serializer
from tastypie import fields, utils
from tastypie.resources import Resource
from tastypie.cache import SimpleCache

from authentication import OAuthAuthentication
from authorization import OAuthAuthorization

from glynt.apps.document.models import Document, ClientCreatedDocument
from glynt.apps.sign.models import DocumentSignature


v1_internal_api = Api(api_name='v1')

available_formats = ['json']


class BaseApiModelResource(ModelResource):
    """
    Base Resource that all other api resources extend
    used to apply our filters and specific rulesets
    """
    class Meta:
        serializer = Serializer(formats=available_formats)
        authentication = OAuthAuthentication()
        authorization = OAuthAuthorization()

    def get_object_list(self, request):
        """ Test for a set of catch field names 
        These keys relate to references to models that need to be filtered by
        the current users company/customer id """
        try:
            self._meta.queryset = self._meta.queryset.model.objects.apply_api_user_filter(request.user)
        except AttributeError:
            pass

        return super(BaseApiModelResource, self).get_object_list(request)


class DocumentResource(BaseApiModelResource):
    class Meta:
        list_allowed_methods = ['get']
        queryset = Document.objects.all()
        resource_name = 'templates'
        serializer = Serializer(formats=available_formats)


class ClientCreatedDocumentResource(BaseApiModelResource):
    class Meta:
        list_allowed_methods = ['get']
        queryset = ClientCreatedDocument.objects.all()
        resource_name = 'documents'
        serializer = Serializer(formats=available_formats)
        excludes = ['body', 'data']
        include_absolute_url = True

    def dehydrate(self, bundle):
        data = ast.literal_eval(bundle.data['meta_data'])
        bundle.data.update(data)
        del(bundle.data['meta_data'])
        return bundle

class SignatureResource(BaseApiModelResource):
    class Meta:
        list_allowed_methods = ['get']
        queryset = DocumentSignature.objects.all()
        resource_name = 'signatures'
        serializer = Serializer(formats=available_formats)
        excludes = ['key_hash', 'hash_data', 'signature']
        include_absolute_url = True

    def dehydrate(self, bundle):
        data = ast.literal_eval(bundle.data['meta_data'])
        bundle.data.update(data)
        del(bundle.data['meta_data'])
        return bundle

""" Register the api resources """
v1_internal_api.register(DocumentResource())
v1_internal_api.register(ClientCreatedDocumentResource())
v1_internal_api.register(SignatureResource())
