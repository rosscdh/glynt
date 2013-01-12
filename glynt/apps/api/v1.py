import ast
from django.conf import settings

from tastypie_elasticsearch.resources import ElasticSearch

from tastypie import fields, utils
from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache
from tastypie.authentication import BasicAuthentication, SessionAuthentication
from tastypie.authorization import Authorization

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


class BaseElasticSearchResource(ElasticSearch):
    class Meta:
        authentication = BasicAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=available_formats)
        es_server = getattr(settings, "ES_INDEX_SERVER", "http://127.0.0.1:9200/")
        es_timeout = 20


class UserTagsResource(BaseElasticSearchResource):
    user = fields.IntegerField(attribute='user', null=False)
    tag = fields.CharField(attribute='tag', null=False)
    class Meta(BaseElasticSearchResource.Meta):
        indices = ["user_tags"]
        resource_name = 'client/tags'


""" Register the api resources """
v1_internal_api.register(DocumentResource())
v1_internal_api.register(ClientCreatedDocumentResource())
v1_internal_api.register(SignatureResource())
v1_internal_api.register(UserTagsResource())
