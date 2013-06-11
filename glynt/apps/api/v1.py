import ast
from itertools import chain
from tastypie.resources import ModelResource, ALL
from tastypie.api import Api
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache
from tastypie.authentication import Authentication, SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization

from django.contrib.auth.models import User

from cities_light.models import City, Country, Region
from glynt.apps.lawyer.models import Lawyer
from glynt.apps.firm.models import Firm, Office
from glynt.apps.startup.models import Startup
from glynt.apps.document.models import DocumentTemplate, ClientCreatedDocument
from glynt.apps.sign.models import DocumentSignature
from glynt.apps.engage.models import Engagement
from glynt.apps.engage import ENGAGEMENT_STATUS

from glynt.apps.startup.bunches import StartupProfileBunch


v1_internal_api = Api(api_name='v1')

available_formats = ['json']


class BaseApiModelResource(ModelResource):
    """
    Base Resource that all other api resources extend
    used to apply our filters and specific rulesets
    """
    class Meta:
        serializer = Serializer(formats=available_formats)
        cache = SimpleCache(timeout=300)
        authentication = SessionAuthentication()


class LocationSimpleResource(BaseApiModelResource):
    name = fields.CharField(attribute='name', null=True)
    region = fields.CharField(attribute='region__name', null=True)

    class Meta(BaseApiModelResource.Meta):
        queryset = City.objects.prefetch_related('region').all()
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'location/lite'
        fields = ['name', 'region']
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        name = bundle.data.get('name', None)
        region = bundle.data.get('region', None)
        bundle.data.pop('name')
        bundle.data.pop('region')
        bundle.data.update({'name': '%s, %s' % (name, region) })
        return bundle


class StateSimpleResource(BaseApiModelResource):
    name = fields.CharField(attribute='display_name', null=True)

    class Meta(BaseApiModelResource.Meta):
        # Only filter by USA, allow freeform for others
        queryset = Region.objects.filter(country_id=Country.objects.get(code3='USA'))
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'state/lite'
        fields = ['display_name',]
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()


class FirmSimpleResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Firm.objects.all()
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'firm/lite'
        fields = ['pk','name']
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()


class OfficeSimpleResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Office.objects.all()
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'office/lite'
        fields = ['pk','address']
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        name = bundle.data.get('address', None)
        bundle.data.pop('address')
        bundle.data.update({'name': name})
        return bundle


class StartupLiteSimpleResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Startup.objects.all()
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'startup/lite'
        fields = ['pk','name', 'website']
        filtering = {
            'name': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        name = bundle.data.get('name', None)
        website = bundle.data.get('website', None)
        bundle.data.pop('name')
        bundle.data.pop('website')
        bundle.data.update({'name': '%s, %s' % (name, website,) })
        return bundle


def _startup_profile(bundle):
    data = StartupProfileBunch(startup=bundle.obj)
    data['profile_photo'] = data.photo_url if data.photo_url else bundle.obj.profile_photo
    data['username'] = bundle.obj.slug # required to integrate with GlyntProfile object
    data['is_startup'] = True
    return data


class StartupBasicProfileResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        queryset = Startup.objects.all().select_related('founders', 'founders_user')
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'startup/profile'

        filtering = {
            'name': ALL,
            'slug': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        profile_data = bundle.data.pop('data')
        bundle.data.update(_startup_profile(bundle))
        return bundle


def _founder_profile(bundle):
    data = {}
    if bundle.obj.profile.is_founder:
        profile = bundle.obj.founder_profile
        try:
            primary_startup = profile.startups[0]
        except IndexError:
            primary_startup = {}

        data.update({
            'profile_url': bundle.obj.founder_profile.get_absolute_url(),
            'summary': profile.summary,
            'bio': profile.bio,
            'startups': [
                {
                    'name': primary_startup.name,
                    'summary': primary_startup.summary,
                    'url': primary_startup.website,
                    'twitter': primary_startup.twitter,
                }
            ],
        })
    return data


def _lawyer_profile(bundle):
    data = {}
    if bundle.obj.profile.is_lawyer:
        profile = bundle.obj.lawyer_profile
        data.update({
            'profile_url': bundle.obj.lawyer_profile.get_absolute_url(),
            'position': profile.position,
            'firm': profile.firm_name,
            'phone': profile.phone,
            'years_practiced': profile.years_practiced,
            'profile_status': profile.profile_status,
            'summary': profile.summary,
            #'fee_packages': profile.fee_packages.items(),
            'practice_locations': profile.practice_locations(),
        })
    return data


class UserBasicProfileResource(BaseApiModelResource):
    name = fields.CharField(attribute='get_full_name', null=True)

    class Meta(BaseApiModelResource.Meta):
        # Only filter by USA, allow freeform for others
        queryset = User.objects.select_related('profile').filter(is_active=True)
        authentication = Authentication()
        list_allowed_methods = ['get']
        resource_name = 'user/profile'
        fields = ['pk','username', 'is_active', 'last_login']
        filtering = {
            'username': ALL,
        }
        cache = SimpleCache()

    def dehydrate(self, bundle):
        profile = bundle.data.get('username', None)
        bundle.data.update({
            'is_lawyer': bundle.obj.profile.is_lawyer,
            'is_founder': bundle.obj.profile.is_founder,
            'profile_photo': bundle.obj.profile.get_mugshot_url(),
            'profile_url': None,
        })
        bundle.data.update(_lawyer_profile(bundle))
        bundle.data.update(_founder_profile(bundle))
        return bundle


class LawyerResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get', 'put', 'patch']
        queryset = Lawyer.objects.all().prefetch_related('user', 'firm_lawyers')
        resource_name = 'lawyers'
        excludes = ['data', 'summary', 'bio']

    def dehydrate(self, bundle):
        bundle.data.pop('role')
        bundle.data['name'] = bundle.obj.user.get_full_name()
        bundle.data['position'] = bundle.obj.position
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


class StartupEngagementResource(BaseApiModelResource):
    lawyer_id = fields.IntegerField('lawyer_id')

    class Meta(BaseApiModelResource.Meta):
        authorization = ReadOnlyAuthorization()
        queryset = Engagement.objects.all()
        resource_name = 'engagement'
        fields = ['lawyer_id', 'engagement_status']
        include_resource_uri = False
        include_absolute_url = True
        filtering = {
            'engagement_status': ALL,
        }

    def authorized_read_list(self, object_list, bundle):
        if not bundle.request.user.is_authenticated():
            return []
        else:
            return object_list.filter(founder=bundle.request.user.founder_profile)

    def dehydrate(self, bundle):
        bundle.data.update({
            'status': ENGAGEMENT_STATUS.get_desc_by_value(bundle.obj.engagement_status).lower(),
        })
        return bundle


""" Register the api resources """
v1_internal_api.register(LocationSimpleResource())
v1_internal_api.register(StateSimpleResource())
v1_internal_api.register(FirmSimpleResource())
v1_internal_api.register(OfficeSimpleResource())
v1_internal_api.register(StartupLiteSimpleResource())

v1_internal_api.register(UserBasicProfileResource())
v1_internal_api.register(StartupBasicProfileResource())

v1_internal_api.register(LawyerResource())
v1_internal_api.register(DocumentResource())
v1_internal_api.register(ClientCreatedDocumentResource())
v1_internal_api.register(SignatureResource())

v1_internal_api.register(StartupEngagementResource())
