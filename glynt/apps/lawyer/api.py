# coding: utf-8
from glynt.apps.api import BaseApiModelResource

from glynt.apps.lawyer.models import Lawyer


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


class LawyerResource(BaseApiModelResource):
    class Meta(BaseApiModelResource.Meta):
        list_allowed_methods = ['get', 'put', 'patch']
        queryset = Lawyer.objects.all().prefetch_related('user', 'firm_lawyers')
        resource_name = 'lawyers'
        excludes = ['data', 'summary', 'bio']

    def dehydrate(self, bundle):
        bundle.data.pop('role')
        bundle.data['name'] = bundle.obj.user.get_full_name()
        bundle.data['position'] = bundle.obj.position
        return bundle