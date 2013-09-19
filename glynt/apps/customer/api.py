# -*- coding: UTF-8 -*-


def _customer_profile(bundle):
    data = {}
    if bundle.obj.profile.is_customer:
        profile = bundle.obj.customer_profile
        try:
            primary_company = profile.companies[0]
        except IndexError:
            primary_company = {}

        data.update({
            'profile_url': bundle.obj.customer_profile.get_absolute_url(),
            'summary': profile.summary,
            'bio': profile.bio,
            'companies': [
                {
                    'name': primary_company.name,
                    'summary': primary_company.summary,
                    'url': primary_company.website,
                    'twitter': primary_company.twitter}
            ],
        })
    return data
