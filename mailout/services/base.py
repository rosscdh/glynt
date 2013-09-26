# -*- coding: utf-8 -*-
from mailout import ABRIDGE_API_URL
from .mixins import UserGetOrCreateMixin


class MailoutConnectionBase(UserGetOrCreateMixin):
    """
    Base Mailout Connection
    """
    client = None
    base_uri = ABRIDGE_API_URL

    def __init__(self, url=None, **kwargs):
        self.base_uri = url if url is not None else self.base_uri

        # append kwargs to class
        self.__dict__.update(kwargs)

        # ensure that we have the current logged in user in abridge
        self.ensure_abridge_user()

    def get_url(self, path):
        return '{base}{path}'.format(base=self.base_uri, path=path)
