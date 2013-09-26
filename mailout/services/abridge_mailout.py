# -*- coding: UTF-8 -*-
from mailout import ABRIDGE_PROJECT

from . import MailoutConnectionBase

import requests
import json


class AbridgeMailoutService(MailoutConnectionBase):
  """
  The Primary Service to interacti with Abridge
  """

  def create_event(self, content, **kwargs):
      data = json.dumps({
        "user_hash": self._user.get('user_hash'),
        "project": ABRIDGE_PROJECT,
        "content": content,
        "data": kwargs
      })

      # query the abridge api
      url = self.get_url(path='event/')
      r = requests.post(url, data, headers=self.headers)

      if r.status_code not in [201]:
          raise Exception('Could not create_event {content}'.format(content=r))

      return r.json()
