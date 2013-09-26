# -*- coding: utf-8 -*-
from mailout import (ABRIDGE_ACCESS_KEY_ID, ABRIDGE_SECRET_ACCESS_KEY,
                     ABRIDGE_USERNAME, ABRIDGE_PASSWORD, ABRIDGE_API_URL)

from .mixins import UserGetOrCreateMixin

import requests


class MailoutConnectionBase(UserGetOrCreateMixin):
    """
    Base Mailout Connection
    """
    base_uri = ABRIDGE_API_URL
    _access_token = None

    def __init__(self, url=None, **kwargs):
        self.base_uri = url if url is not None else self.base_uri

        # append kwargs to class
        self.__dict__.update(kwargs)

        # ensure that we have the current logged in user in abridge
        self.ensure_abridge_user()

    @property
    def headers(self):
        return {
            'Authorization': 'Bearer {access_token}'.format(access_token=self.access_token),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @property
    def access_token(self):
        """
        Get the all important access_token
        """
        # if we dont already have the token
        if self._access_token is None:
            # content defined so we can test for response
            content = {}

            # set std form post headers for the auth token request
            headers = {
                'Content-type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            }

            data = {
                'client_id': ABRIDGE_ACCESS_KEY_ID,
                'client_secret': ABRIDGE_SECRET_ACCESS_KEY,
                'grant_type': 'password',
                'username': ABRIDGE_USERNAME,
                'password': ABRIDGE_PASSWORD,
            }

            # query the abridge api
            url = self.get_url(path='oauth2/access_token/')
            r = requests.post(url, data, headers=headers)

            if r.status_code in [200]:
                content = r.json()
                self._access_token = content.get('access_token')

            if content.get('access_token', None) is None:
                raise Exception('Could not obtain access_token: {content}'.format(content=r))

        return self._access_token

    def get_url(self, path):
        return '{base}{path}'.format(base=self.base_uri, path=path)
