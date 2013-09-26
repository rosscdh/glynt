# -*- coding: utf-8 -*-
from mailout import ABRIDGE_PROJECT

import requests
import hashlib
import json


class UserGetOrCreateMixin(object):
    """
    The User Mixin that allows us to communicate with Abridge as a user
    """
    _user = None
    _email_hash = None

    def ensure_abridge_user(self):
        """
        Get the mailout user, based on our current django user
        """
        if self._user is None:
            # create a hash from the current users email address
            self._email_hash = hashlib.md5(self.user.email).hexdigest()

            # query the abridge api
            url = self.get_url(path='user/{email_hash}/'.format(email_hash=self._email_hash))
            r = requests.get(url, headers=self.headers)

            if r.status_code in [404]:  # 404 not found
                self._user = self.create_user()
            else:
                self._user = r.json()

        self.subscribe()

        return self._user

    def create_user(self):
        """
        If the abridge version of our user does not exist then create them
        """
        # setup data
        user_data = json.dumps({
            'username': self.user.username,
            'email': self.user.email
        })

        # query the abridge api
        url = self.get_url(path='user/')
        r = requests.post(url, user_data, headers=self.headers)

        if r.status_code not in [201]:  # 201 created
            raise Exception('{status_code}: Could not create user: {content}'.format(status_code=r.status_code, content=r.content))

        return r.json()

    def subscribe(self):
        """
        Ensure that the current user has subscribed to our project
        """
        content = None
        # get existing subscriptions
        subscriptions = self._user.get('subscriptions', [])

        if len(subscriptions) == 0 or ABRIDGE_PROJECT not in subscriptions:
            # add our project subscription
            subscriptions.append(ABRIDGE_PROJECT)

            # setup data
            subscription_data = json.dumps({
                'subscriptions': subscriptions
            })

            # query the abridge api
            url = self.get_url(path='user/{user_hash}/'.format(user_hash=self._user.get('user_hash')))
            r = requests.patch(url, subscription_data, headers=self.headers)

            if r.status_code not in [200]:
                raise Exception('{status_code}: Could not subscribe to {subscription}: {content}'.format(status_code=r.status_code, subscription=ABRIDGE_PROJECT, content=r))

        return content
