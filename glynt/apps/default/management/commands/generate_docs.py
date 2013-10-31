# 2013.10.25 17:05:06 CEST
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from bunch import Bunch
import os
import os.path


class Command(BaseCommand):
    help = 'Generate documents for the glynt apps'
    formats = ['.py', '.js']
    base_doc_path = './docs/'
    base_apps_path = './glynt/apps/'

    def files(self):
        c = 0
        apps = {}
        for dirpath, dirnames, filenames in os.walk(self.base_apps_path):
            if c == 0:
                for a in dirnames:
                    apps[a] = []


            current_app = dirpath.split('/')
            current_app = [:1]
            import pdb;pdb.set_trace()
            for format in self.formats:
                files = [f for f in filenames if f.endswith(format)]

            # for f in files:
            #     yield 'pycco -d {base_doc_path}{app} ./glynt/apps/{app}/*{format}'.format(base_doc_path=self.base_doc_path, app=dirpath, format=format)
            c = c+1




    def handle(self, *args, **options):
        for c in self.files():
            print c
