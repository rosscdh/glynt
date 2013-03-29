import ast

from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache
from tastypie.authentication import Authentication, SessionAuthentication

from glynt.apps.firm.models import Firm, Office
from glynt.apps.document.models import DocumentTemplate, ClientCreatedDocument
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
        cache = SimpleCache(timeout=30)
        authentication = SessionAuthentication()

    def get_object_list(self, request):
        """ Test for a set of catch field names 
        These keys relate to references to models that need to be filtered by
        the current user"""
        try:
            self._meta.queryset = self._meta.queryset.model.objects.apply_api_user_filter(request.user)
        except AttributeError:
            pass

        return super(BaseApiModelResource, self).get_object_list(request)


class FirmSimpleResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        authentication = Authentication()
        list_allowed_methods = ['get']
        queryset = Firm.objects.all()
        resource_name = 'firm'
        includes = ['pk','name']


class OfficeSimpleResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        authentication = Authentication()
        list_allowed_methods = ['get']
        queryset = Office.objects.all()
        resource_name = 'office'
        includes = ['pk','address']

    def dehydrate(self, bundle):
        name = bundle.data.get('address', None)
        bundle.data.pop('address')
        bundle.data.update({'name': name})
        return bundle

class DocumentResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        list_allowed_methods = ['get']
        queryset = DocumentTemplate.objects.all()
        resource_name = 'document/templates'
        excludes = ['body']


class ClientCreatedDocumentResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        list_allowed_methods = ['get']
        queryset = ClientCreatedDocument.objects.all()
        resource_name = 'client/documents'
        excludes = ['body', 'data']
        include_absolute_url = True

    def dehydrate(self, bundle):
        data = ast.literal_eval(bundle.data['meta_data'])
        bundle.data.update(data)
        del(bundle.data['meta_data'])
        return bundle


class SignatureResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        list_allowed_methods = ['get']
        queryset = DocumentSignature.objects.all()
        resource_name = 'client/signatures'
        excludes = ['key_hash', 'hash_data', 'signature']
        include_absolute_url = True

    def dehydrate(self, bundle):
        data = ast.literal_eval(bundle.data['meta_data'])
        bundle.data.update(data)
        del(bundle.data['meta_data'])
        return bundle


""" Register the api resources """
v1_internal_api.register(FirmSimpleResource())
v1_internal_api.register(OfficeSimpleResource())

v1_internal_api.register(DocumentResource())
v1_internal_api.register(ClientCreatedDocumentResource())
v1_internal_api.register(SignatureResource())
