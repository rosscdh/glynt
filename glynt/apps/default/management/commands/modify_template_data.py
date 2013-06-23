# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand

from glynt.apps.document.models import DocumentTemplate, ClientCreatedDocument


class Command(BaseCommand):
    help = 'Updates Template body: effectively search/replace'
    search = None
    replace = None
    def handle(self, *args, **options):
        try:
            search = args[0]
            replace = args[1]
        except IndexError:
            print("You need to define search and replace manage.py modify_template_data <search> <replace>")
            sys.exit(0)
        c = 0
        for i in DocumentTemplate.objects.all():
            i.body = i.body.replace(search, replace)
            i.save()
            c += 1

        d = 0
        for i in ClientCreatedDocument.objects.all():
            i.body = i.body.replace(search, replace)
            i.save()
            d += 1


        self.stdout.write('Successfully cleaned %d models "%s"' % (c, 'DocumentTemplate',) )
        self.stdout.write('Successfully cleaned %d models "%s"' % (d, 'ClientCreatedDocument',) )