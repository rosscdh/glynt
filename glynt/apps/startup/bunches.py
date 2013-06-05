# -*- coding: utf-8 -*-
from bunch import Bunch

import logging
logger = logging.getLogger('lawpal.services')


class StartupProfileBunch(Bunch):
    def __init__(self, startup):
        data = startup.data
        return super(StartupProfileBunch, self).__init__(
                    status = data.get('status'), 
                    community_profile =  False, 
                    crunchbase_url =  data.get('crunchbase_url'), 
                    video_url =  data.get('video_url'), 
                    angellist_url = data.get('angellist_url'),
                    high_concept = data.get('high_concept'),
                    locations = [i.get('display_name') for i in data.get('locations', [])],
                    markets =  [i.get('display_name') for i in data.get('markets', [])],
                    thumb_url = data.get('thumb_url'),
                    photo_url = data.get('photo_url'),
                    screenshots = [s for s in data.get('screenshots', [])],
                )