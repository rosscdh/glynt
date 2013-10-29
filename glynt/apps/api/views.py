# -*- coding: UTF-8 -*-
from rest_framework.test import APIClient
import json


class v2ApiClientMixin(object):
    """
    Mixin to allow us to replicate a query to the API
    which allows us to prepopulate the view with JSON data thats
    exactly the same as would be gotten by querying the API
    """
    api_client = None
    api_uri = None
    api_resp = None

    def __init__(self, *args, **kwargs):
        """
        set the api_client var
        """
        self.api_client = APIClient()
        super(v2ApiClientMixin, self).__init__(*args, **kwargs)

    def api_query(self, request, url=None, method='get', **kwargs):
        url = url if url is not None else self.api_uri

        if 'format' not in kwargs:
            kwargs.update({
                'format': 'json'
            })

        assert url is not None, "You must pass in a url=':path' or specify api_uri on this view"

        user = request.user
        self.api_client.force_authenticate(user=user)  # authenticate as current user
        # get the method to call (get,list,put,patch,delete)
        method = getattr(self.api_client, method)

        self.api_resp = method(url, **kwargs)

        return self

    def api_resp_as_json(self):
        return json.loads(self.api_resp.content)