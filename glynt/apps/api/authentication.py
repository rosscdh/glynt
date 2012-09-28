from tastypie.authentication import Authentication

#from platform.apps.authorize.models import OauthAccessToken, OauthClient
from django.shortcuts import get_object_or_404


class OAuthAuthentication(Authentication):
    """ Method to check that the facebook token specified returns only the data valid for that token """
    def is_authenticated(self, request, **kwargs):
        """@TODO this method needs to be updated to use the facebook access_token """
        access_token = request.GET.get('access_token')
        if not access_token:
            return False

        # try:
        #     token = get_object_or_404(OauthAccessToken, code=access_token)
        # except OauthAccessToken.DoesNotExist:
        #     #@TODO need to add logging
        #     return False

        # if not token or not token.is_valid():
        #     return False

        return True

    # Optional but recommended
    # def get_identifier(self, request):
    #     return request.user.company.name
