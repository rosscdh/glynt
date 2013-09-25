# -*- coding: UTF-8 -*-
from django.conf import settings

import json

from . import MailoutConnectionBase


class AbridgeMailoutService(MailoutConnectionBase):
    def create_event(self, content, **kwargs):
        event_data = {
          "user_hash": self._user.get('user_hash'),
          "project": settings.ABRIDGE_PROJECT,
          "content": content,
          "data": kwargs
        }

        resp, content = self.request(path='event/', data=event_data, method='POST')

        if resp.status not in [201]:
            raise Exception('Could not create_event {content}'.format(content=content))

        return json.loads(content)