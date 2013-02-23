# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand

from glynt.apps.document.models import DocumentHTML
from glynt.apps.document.models import DocumentTemplate
from glynt.apps.smoothe.pybars_smoothe import Smoothe


class InvalidTemplateException(Exception):
    def __init__(self, doc_id, msg):
        msg = '%s. Threw Exception: %s' % (doc_id, msg,)
        super(self, InvalidTemplateException).__init__(**{'msg': msg})


class Command(BaseCommand):
    help = 'Import & Validate templates: from file.md or from the database'

    def handle(self, *args, **options):
        # from file or from db
        if len(args) > 0:
            # probably a list of ids
            id_list = args[0].split(',')
            if len(id_list) > 0:
                self.from_db(id_list)
            else:
                # looks like a queryset filter
                self.from_db(args)
        elif len(options) > 0:
            # probably a set of queryset filters
            pass

    def from_file(self, path):
        raise Exception('You must pass in a valid path to a directory of filenames.md')
        for f in fileset:
            self.validate(doc_id='Template Files: %s' %(f.abspath,) , f.read())

    def from_db(self, params):
        resultset = None
        #if is a dict then is a querysetfilter
        if type(params) is dict:
            resultset = DocumentTemplate.objects.filter(**params)
        # if is a list then is list of ids
        if type(params) is list:
            # ensure we have only ids
            id_list = [id for id in params is type(id) is int]
            resultset = DocumentTemplate.objects.filter(pk=id_list)

        if resultset is None:
            raise Exception('You must pass in a list of ids [1,2,...] or a set of queryset filters slug=confidential-monkey-doc')
        else:
            for t in resultset:
                self.validate(doc_id='Database Template: %s (%d)' %(t.id, t.name,) , document_html)

    def validate(self, doc_id, document_html):
        smoothe = Smoothe(source_html=document_html)
        try:
            smoothe.render({})
        except Exception as e:
            raise InvalidTemplateException(doc_id=doc_id, msg=e)
