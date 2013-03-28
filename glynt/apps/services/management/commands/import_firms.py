# -*- coding: utf-8 -*-
import os
from django.db.utils import IntegrityError
from optparse import make_option
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode

from glynt.apps.firm.models import Firm, Office

import csv
import pdb

class Command(BaseCommand):
    """ Imports Firms from the GDrive FirmsDB spreadsheet
    initially as a dwnloaded csv but eventually directly from gdocs """
    option_list = BaseCommand.option_list + (
        make_option('--local_file',
            action='store_true',
            dest='local_file',
            default='/Users/rossc/Downloads/LawyerDB-Firms.csv',
            help='Path to the local csv file'),
        )
    local_file = None

    def handle(self, *args, **options):
        self.local_file = options['local_file']

        if self.local_file and os.path.exists(self.local_file):
            self.import_csv(self.local_file)
        else:
            print "could not find file at: %s" % self.local_file

    def import_csv(self, csv_file):
        """
        [''Firm Name', 'Address', 'Cities']
        """
        with open(csv_file, 'rb') as csv_file:
            print "starting csv"
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
            for i,r in enumerate(csv.reader(csv_file, dialect)):
                # get nice names
                for k,v in enumerate(r):
                    r[k] = smart_unicode(v)
                firm_name, address, cities, = r

                firm, firm_is_new = Firm.objects.get_or_create(name=firm_name)
                office, office_is_new = Office.objects.get_or_create(firm=firm, address=address)

