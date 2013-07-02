# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import json

from glynt.apps.flyform.models import FlyForm


class Command(BaseCommand):
    help = 'Fixes any Fixtures that are not correctly encoded'
    json_fields = ['body', 'data']
    def handle(self, *args, **options):
        for i in FlyForm.objects.all():
            if type(i.body) is not list:
                body = i.body.encode("utf-8")
                body = body.decode('string_escape')
                i.body = json.dumps(body)
                i.save()


        self.stdout.write('Successfully cleaned model "%s"' % ('Flyform') )