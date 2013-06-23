# -*- coding: utf-8 -*-
from django.core.files.base import File

from PIL import Image
import StringIO

import logging
logger = logging.getLogger('django.request')


class PhotoDownloadService(object):
    """ Service to download and store photos """
    url = None
    file_name = None
    downloaded_file = None
    def __init__(self, url, file_name, **kwargs):
        self.url = url
        self.file_name = file_name
        self.downloaded_file = File(self.download(self.url), name=self.file_name)

    def download(self, url):
        req = requests.get(url)
        return Image.open(StringIO.StringIO(req.content))
